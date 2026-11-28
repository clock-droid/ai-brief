// Read-only Aside REPL. Python supplies input as JSON on each invocation.
function brief(t) {
  const handle = t.author.screenName;
  return {
    id: t.id, author: handle, url: "https://x.com/" + handle + "/status/" + t.id,
    published: new Date(t.createdAt).toISOString(), text: t.text.slice(0, 900),
    parent: t.inReplyToId || null,
    metrics: {likes: t.likes, retweets: t.retweets, views: t.views}
  };
}

// The text an original post starts with, as it appears inside "RT @author: …" (whitespace collapsed).
function head(text) {
  return text.replace(/\s+/g, " ").replace(/…$/, "").trim().slice(0, 60);
}

if (input.user) {
  // Posts tab: the account's own posts and retweets, newest first (a pinned post may lead).
  let cursor;
  let complete = false;
  for (let page = 0; page < 5; page++) {
    const result = await twitter.getUserTweets(input.user, {count: 20, cursor});
    for (const tweet of result.tweets) {
      if (new Date(tweet.createdAt) < new Date(input.since)) continue;
      const rt = tweet.text.match(/^RT @(\w+): ([\s\S]*)$/);
      if (rt) {
        // A retweet: the original id is not exposed, so report who amplified what; Python finds the original later.
        if (rt[1].toLowerCase() !== input.user.toLowerCase())
          console.log("AMP " + JSON.stringify({by: input.user, author: rt[1], prefix: head(rt[2]),
                                                at: new Date(tweet.createdAt).toISOString()}));
        continue;
      }
      const row = brief(tweet);
      if (tweet.quotedTweet) row.quoted = brief(tweet.quotedTweet);
      console.log("ROW " + JSON.stringify(row));
    }
    // A pinned post can be old, so only the page's last post marks the end of the window.
    const last = result.tweets.at(-1);
    const older = last && new Date(last.createdAt) < new Date(input.since);
    if (older || !result.nextCursor || !result.tweets.length) { complete = true; break; }
    if (cursor === result.nextCursor) break;
    cursor = result.nextCursor;
  }
  console.log("END " + JSON.stringify(complete));
} else if (input.query) {
  let cursor;
  const seen = new Set();
  let complete = false;
  for (let page = 0; page < 5; page++) {
    const result = await twitter.search(input.query, {count: 30, product: "Latest", cursor});
    for (const tweet of result.tweets) {
      if (seen.has(tweet.id)) continue;
      seen.add(tweet.id);
      const row = brief(tweet);
      if (tweet.quotedTweet) row.quoted = brief(tweet.quotedTweet);
      console.log("ROW " + JSON.stringify(row));
    }
    if (!result.nextCursor || !result.tweets.length) { complete = true; break; }
    if (cursor === result.nextCursor) break;
    cursor = result.nextCursor;
  }
  console.log("END " + JSON.stringify(complete));
} else if (input.match) {
  // Find retweeted originals on the original author's Posts tab by their opening text.
  const left = new Set(input.match.prefixes);
  let cursor;
  for (let page = 0; page < 3 && left.size; page++) {
    const result = await twitter.getUserTweets(input.match.author, {count: 40, cursor});
    for (const tweet of result.tweets) {
      if (tweet.text.startsWith("RT @")) continue;
      const text = head(tweet.text);
      for (const prefix of left) {
        if (text.startsWith(prefix) || (text.length >= 20 && prefix.startsWith(text))) {
          left.delete(prefix);
          const row = brief(tweet);
          row.prefix = prefix;
          if (tweet.quotedTweet) row.quoted = brief(tweet.quotedTweet);
          console.log("ROW " + JSON.stringify(row));
        }
      }
    }
    if (!result.nextCursor || !result.tweets.length || cursor === result.nextCursor) break;
    cursor = result.nextCursor;
  }
  console.log("END true");
} else {
  for (const id of input.ids) {
    try {
      console.log("ROW " + JSON.stringify(brief(await twitter.getTweet(id))));
    } catch (error) {
      if (String(error).includes("HTTP 429")) throw error;
      // Keep the parent permalink for manual verification when the API has no text.
    }
  }
  console.log("END true");
}
