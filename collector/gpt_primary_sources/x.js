// Read-only Aside REPL. Python supplies input as JSON on each invocation.
function brief(t) {
  const handle = t.author.screenName;
  return {
    id: t.id, author: handle, url: "https://x.com/" + handle + "/status/" + t.id,
    published: new Date(t.createdAt).toISOString(), text: t.text.slice(0, 900),
    parent: t.inReplyToId || null
  };
}

if (input.query) {
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
