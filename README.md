# NAFCoin
這東西主要由 https://discord.gg/nafstore 推廣使用，委託者為 https://nafstore.net

邀請連結：~~https://ptb.discord.com/api/oauth2/authorize?client_id=1109155698631250060&permissions=0&scope=bot%20applications.commands~~ 已失效
# 功能介紹
1. 每日簽到功能
- 指令：/sign每日簽到
- 描述：每日簽到，獲得 NAF Coin 1 ~ 15 枚
- 說明：
  - 確認帳號已滿 30 天才能進行簽到
  - 簽到完成後，會給予隨機數量的 NAF Coin，範圍介於 1 到 15 枚之間
  - 會記錄簽到紀錄和點數變動日誌
2. 點數轉贈功能
- 指令：/give點數轉贈
- 描述：轉贈 NAF Coin 給其他人
- 參數：
  - member：轉贈對象（必填）
  - point：轉贈 NAF Coin 數量（必填，最少 300 枚）
- 說明：
  - 轉贈前會檢查轉贈對象是否為機器人或自己
  - 轉贈時會檢查轉贈者是否擁有足夠的 NAF Coin
  - 轉贈成功後，會扣除轉贈者的點數並給予接收者對應的點數
  - 會記錄點數變動日誌
3. 查詢點數功能
- 指令：/point查詢點數
- 描述：查詢自己（或他人）的 NAF Coin 點數
- 參數：
  - search_member：查詢對象（選填，留空代表查詢自己）
- 說明：
  - 查詢自己或他人的 NAF Coin 點數
  - 會顯示該使用者擁有的 NAF Coin 數量
4. 前十排行榜功能
- 指令：/top前十排行榜
- 描述：列出前十名 NAF Coin 持有者
- 說明：
  - 顯示持有 NAF Coin 數量最多的前十位使用者
  - 會顯示目前的總發行 NAF Coin 數量和總參與人數
5. 兌換商品功能
- 指令：/redeem兌換商品
- 描述：把 NAF Coin 換成喜歡的形狀！
- 參數：
id：商品序號（選填，留空可查詢現可兌換商品）
- 說明：
  - 如果提供商品序號，則進行兌換商品的動作
  - 檢查是否有庫存以及使用者是否有足夠的 NAF Coin
  - 兌換成功後，會給予兌換碼並扣除相應的點數
  - 會記錄點數變動日誌和兌換紀錄
# 注意事項
- 請在程式碼中的 bot.run() 函式中填入您的 Discord 機器人的 Token 來啟動機器人。
- 基於 Pycord 開發，安裝請見 https://docs.pycord.dev/en/stable/installing.html
- 程式碼中使用到的模組 point_ext 是自定義模組，但因為程式碼真的寫太糟所以不太想丟出來（雖然主程式也很糟就對了）
- 如果有任何問題或錯誤，歡迎開 issue 或是透過 https://kangjw.me/ 上面的聯繫方式聯絡我
- 希望這個程式對您有所幫助，祝您使用愉快！

