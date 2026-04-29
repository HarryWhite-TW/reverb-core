# Public API Surface Note（v0.6 → v0.7 pre-freeze）

## 1. 這份文件是做什麼的
這份文件用來說明：`preprocess_input()` 目前有哪些對外承諾，已經可以先視為 v0.7 前的最小穩定 public API surface。

## 2. 目前已固定的最小 public surface
目前可先視為最小穩定對外承諾的內容如下：

- `preprocess_input(...)` 會回傳 `ProcessingResult`
- `correlation_id` 一定存在
- `original_input` 會保留原始輸入
- `processed_text` 一定存在，且型別為字串
- `is_valid` 一定存在，且型別為布林值
- `events` 一定存在，且型別為 list
- `errors` 一定存在，且型別為 list

這些內容目前已被測試保護，可先視為 v0.7 前的最小穩定 public surface。

## 3. 目前已正式涵蓋的代表輸入類型
目前先用以下三種輸入類型，作為 public API surface 的最小代表面：

- valid input
- empty / fallback input
- non-string input

選這三類的原因是：

- valid input 代表正常成功路徑
- empty / fallback input 代表空輸入與 early return 路徑
- non-string input 代表 type_guard 攔截與非字串失敗路徑

也就是說，目前的最小 public surface，不是想涵蓋所有細節案例，而是先固定三種最核心、最能代表系統對外行為的輸入面。

## 4. 目前還沒有 freeze 的部分
以下內容目前還不算完整 freeze 範圍，因此暫時不能當成最終對外承諾：

- 每個 `event` 的完整順序是否逐一固定
- `error message` 的完整文字是否逐字固定
- `profile / config` 進入核心後的公共行為
- adapter / SDK 外部接法
- package 層級的正式使用方式

也就是說，現在先固定的是最小 public surface，而不是整個未來 SDK 的所有細節。

## 5. 下一步預計收斂方向
這份文件目前只是 v0.7 Public API / Contract Freeze 前的 pre-freeze note。

下一步預計要繼續確認：

- 哪些欄位要正式列入 v0.7 public API
- 哪些錯誤碼與 event 名稱要正式固定
- profile / config 是否要進入最小 public behavior
- 未來若建立 adapter / SDK 外部接法，應如何維持目前的 `ProcessingResult` contract

目前這份 note 的重點不是完整定義未來 SDK，而是先把已經測試保護、已經相對穩定的最小 public surface 說清楚。

## 6. 對照檢查

這份 note 的內容需要和目前的 contract、測試檔保持一致。

目前先確認以下最小對照：

| 文件中的承諾 | 程式來源 | 測試來源 | 目前判斷 |
| --- | --- | --- | --- |
| `preprocess_input(...)` 會回傳 `ProcessingResult` | `src/elysia_core/input/preprocess.py` / `ProcessingResult` | `test_preprocess_input_returns_stable_processing_result_surface_for_valid_input` | 已對齊 |
| `correlation_id` 一定存在，且型別為字串 | `ProcessingResult` | `test_processing_result_exposes_minimum_public_fields` | 已對齊 |
| `original_input` 會保留原始輸入 | `ProcessingResult` | `test_processing_result_exposes_minimum_public_fields` | 已對齊 |
| `processed_text` 一定存在，且型別為字串 | `ProcessingResult` | `test_processing_result_exposes_minimum_public_fields` | 已對齊 |
| `is_valid` 一定存在，且型別為布林值 | `ProcessingResult` | `test_processing_result_exposes_minimum_public_fields` | 已對齊 |
| `events` 一定存在，且型別為 list | `ProcessingResult` | `test_processing_result_exposes_minimum_public_fields` | 已對齊 |
| `errors` 一定存在，且型別為 list | `ProcessingResult` | `test_processing_result_exposes_minimum_public_fields` | 已對齊 |
| `StepEvent` 至少保留 `name / severity / changed` | `StepEvent` | `test_step_event_exposes_minimum_observable_fields` | 已對齊 |
| `ErrorItem` 至少保留 `code / message / step / severity` | `ErrorItem` | `test_error_item_exposes_minimum_machine_readable_fields` | 已對齊 |

這段對照的目的，是避免文件承諾超過目前 code 與 tests 實際保護的範圍。