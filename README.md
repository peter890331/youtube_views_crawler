# youtube_views_crawler
以 Selenium 爬蟲 YouTube 頻道的長影片與短影音觀看次數。

### ❗以ChatGPT開發，僅供Selenium與爬蟲練習。❗

以 Windows 電腦，    
在 Releases 下載 youtube_views_crawler.exe，    
並下載 [ChromeDriver][1]，解壓縮 chromedriver-win64.zip 後，    
將 chromedriver.exe 和 youtube_views_crawler.exe 置於同個資料夾，如下，

 <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/%E8%B3%87%E6%96%99%E5%A4%BE%E9%A0%90%E8%A8%AD.png" width="500px">

雙擊 youtube_views_crawler.exe 開啟程式，    
輸入欲爬蟲的 YouTube 頻道 ID，如下紅框中的字串，並按下 Enter，

 <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/%E9%A0%BB%E9%81%93ID.png" width="500px">

 等待爬蟲完成，過程如下，

 <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/%E7%88%AC%E8%9F%B2%E9%81%8E%E7%A8%8B.png" width="500px">

 爬蟲完成後，會出現一個 results 資料夾，爬蟲結果的頻道公開影片觀看次數折線圖.png 會在其中，例如：

 <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/results/%40peter0331_%E9%A0%BB%E9%81%93%E5%85%AC%E9%96%8B%E5%BD%B1%E7%89%87%E8%A7%80%E7%9C%8B%E6%AC%A1%E6%95%B8%E6%8A%98%E7%B7%9A%E5%9C%96.png" width="500px">
  <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/results/%40nsfwstudio_%E9%A0%BB%E9%81%93%E5%85%AC%E9%96%8B%E5%BD%B1%E7%89%87%E8%A7%80%E7%9C%8B%E6%AC%A1%E6%95%B8%E6%8A%98%E7%B7%9A%E5%9C%96.png" width="500px">
    <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/results/%40Muyao4_%E9%A0%BB%E9%81%93%E5%85%AC%E9%96%8B%E5%BD%B1%E7%89%87%E8%A7%80%E7%9C%8B%E6%AC%A1%E6%95%B8%E6%8A%98%E7%B7%9A%E5%9C%96.png" width="500px">
      <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/results/%40MrBeast_%E9%A0%BB%E9%81%93%E5%85%AC%E9%96%8B%E5%BD%B1%E7%89%87%E8%A7%80%E7%9C%8B%E6%AC%A1%E6%95%B8%E6%8A%98%E7%B7%9A%E5%9C%96.png" width="500px">
        <img src= "https://github.com/peter890331/youtube_views_crawler/blob/figures/results/%40dinosaurnobrain_%E9%A0%BB%E9%81%93%E5%85%AC%E9%96%8B%E5%BD%B1%E7%89%87%E8%A7%80%E7%9C%8B%E6%AC%A1%E6%95%B8%E6%8A%98%E7%B7%9A%E5%9C%96.png" width="500px">

[1]: https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.94/win64/chromedriver-win64.zip
