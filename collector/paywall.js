// Aside REPL: 로그인된 Aside 브라우저로 기사 하나를 열어 본문 문단을 읽는다 (읽기 전용).
// Python(mac_paywall.py)이 input = {url}을 앞에 붙여 실행한다.
const page = await openTab(input.url);
try {
  await page.waitForSelector("p[data-type=paragraph]", {timeout: 20000}).catch(() => {});
  await page.waitForTimeout(3000);
  const result = await page.evaluate(() => {
    const paragraphs = [...document.querySelectorAll("p[data-type=paragraph]")]
      .map(p => p.innerText.trim()).filter(Boolean);
    const head = document.body.innerText.slice(0, 4000);
    return {
      title: document.title.replace(/ - WSJ$/, ""),
      paragraphs,
      // 로그인이 풀리면 앞 두세 문단과 구독·로그인 안내만 보인다
      locked: paragraphs.length <= 3 && /Sign In|Subscribe|Continue reading your article/i.test(head),
    };
  });
  console.log("RESULT " + JSON.stringify(result));
} finally {
  await page.close();
}
