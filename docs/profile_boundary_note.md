# Profile Boundary Note（v0.7 pre-design）

## 1. 這份文件是做什麼的

這份文件用來說明：目前 `config_loader.py` 和 `validator.py` 只是 config/profile 的前置材料，還不是 `preprocess_input()` 的 runtime public behavior。

它的目的，是先區分：

- 哪些設定目前只是 config validation
- 哪些設定未來可能成為 Minimal Policy Profile
- 哪些設定目前偏離 Reverb Core 的 input guardrail 主線

## 2. 目前只屬於 config validation 的設定

以下設定目前只視為 config validation，不視為 Reverb guardrail 的 policy profile：

- `persona_name`
- `max_response_length`

原因是：它們目前只被 validator 檢查合法性，尚未影響 `preprocess_input()` 的實際處理行為。

## 3. 未來可能成為 Minimal Policy Profile 的候選設定

以下設定如果未來接入 `preprocess_input()`，可能會影響 guardrail 行為，因此可以視為 policy profile 候選：

- `fallback_text`
- `enable_symbol_cleaner`
- `max_input_length`

原因是：它們可能影響 fallback 輸出、pipeline step 是否執行，或輸入長度限制。

## 4. 目前不應納入 Reverb Core profile 的設定

以下設定目前偏離 Reverb Core 的 input guardrail 主線：

- `ui_theme`

原因是：Reverb Core 目前不是 UI 應用，`ui_theme` 不影響 input preprocessing 或 guardrail behavior。

## 5. 目前邊界判斷

目前 `validator.py` 有 unit tests 保護自己的 fallback 行為，但它尚未接入 `preprocess_input()`。

因此它目前不應被寫入 public API freeze 範圍，也不應被視為已完成的 Minimal Policy Profile。

下一步若要推進 profile，應先設計最小 policy surface，再決定是否接入 runtime。