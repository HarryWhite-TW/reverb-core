# Fallback Text Policy Note（v0.7 pre-design）

## 1. 這份文件是做什麼的

這份文件用來說明：如果未來 `fallback_text` 進入 Minimal Policy Profile，它應該影響哪些行為，以及不應該影響哪些 contract。

目前這份文件只是設計草稿，不代表 `fallback_text` 已經接入 runtime。

## 2. 目前現況

目前 `preprocess_input()` 的 fallback 輸出文字固定為 `…`。

目前至少有兩種 fallback 路徑會使用這個安全輸出：

- 非字串輸入會被 `type_guard` 擋下
- 空輸入會觸發 `fallback_if_empty`

## 3. `fallback_text` 的預期用途

`fallback_text` 未來如果成為 policy profile 設定，應只用來決定 fallback 時的安全輸出文字。

也就是說，它只應影響：

- fallback 路徑中的 `processed_text`
- fallback event 中的 `after` 值

## 4. `fallback_text` 不應影響的內容

即使未來 `fallback_text` 可以設定，它也不應該改變以下 contract：

- `is_valid` 仍應為 `False`
- `errors` 仍應保留原本的錯誤身份
- `EMPTY_INPUT` 不應因 fallback text 改變而消失
- `UNEXPECTED_TYPE` 不應因 fallback text 改變而消失
- `fallback_if_empty` event name 不應改變
- `type_guard` event name 不應改變
- `original_input` 仍應保留原始輸入
- `correlation_id` 仍應正常產生

## 5. 為什麼先選 `fallback_text`

`fallback_text` 是較低風險的 policy profile 候選。

原因是：它主要影響 fallback 輸出文字，不會改變整條 pipeline 的執行順序。

相較之下：

- `enable_symbol_cleaner` 會影響正常輸入的正規化結果
- `max_input_length` 需要先設計超過長度時要拒絕、截斷、fallback，或產生新的 ErrorItem

因此 `fallback_text` 比較適合作為第一個 Minimal Policy Profile 設計候選。

## 6. 尚未決定的問題

目前仍未決定：

- `fallback_text` 應該放在哪個 config/profile 結構中
- `fallback_text` 是否允許空字串
- `fallback_text` 若不是字串時應如何處理
- `fallback_text` 是否應同時影響 `type_guard` 與 `fallback_if_empty`
- 未來測試應放在 unit、contract，還是 integration 層

## 7. 下一步

下一步不應直接改 runtime。

應先完成：

1. 明確定義 `fallback_text` 的最小 policy surface
2. 設計對應測試案例
3. 再決定是否接入 `preprocess_input()`