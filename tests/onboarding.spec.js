describe('QualGent Homepage Test', () => {
  it('should load homepage and check title', async () => {
    await browser.url('https://qualgent-frontend-xyz123.web.app');  // change to actual deployed frontend
    const title = await browser.getTitle();
    console.log('Page title is:', title);
  });
});
