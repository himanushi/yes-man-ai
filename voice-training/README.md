# Yes Man 音声学習ガイド

## セットアップ

### 1. 依存パッケージのインストール

```bash
cd voice-training
uv sync
```

## 学習手順

### ステップ1: 動画から音声を抽出

動画ファイルを `data/raw/` に配置してから実行：

```bash
uv run python scripts/extract_audio.py
```

オプション:
- `--input`: 入力ディレクトリ（デフォルト: `../data/raw`）
- `--output`: 出力ディレクトリ（デフォルト: `../data/processed/extracted`）
- `--format`: 出力形式（デフォルト: `wav`）

### ステップ2: 音声データの前処理

抽出した音声を学習用に前処理：

```bash
uv run python scripts/prepare_data.py
```

この処理で以下を実行：
- 無音区間の除去
- 音量正規化
- ノイズ除去
- セグメント分割（1-10秒）

オプション:
- `--input`: 入力ディレクトリ（デフォルト: `../data/processed/extracted`）
- `--output`: 出力ディレクトリ（デフォルト: `../data/processed/training`）
- `--sr`: サンプリングレート（デフォルト: `16000`）

### ステップ3: メタデータ生成（文字起こし）

音声ファイルからテキストを自動抽出してmetadata.csvを生成：

```bash
uv run python scripts/create_metadata.py
```

この処理でWhisperを使用して各音声ファイルを文字起こしします。

オプション:
- `--audio`: 音声ファイルディレクトリ（デフォルト: `../data/processed/training`）
- `--output`: 出力CSVパス（デフォルト: `../data/processed/training/metadata.csv`）
- `--model`: Whisperモデルサイズ（デフォルト: `base`、選択肢: `tiny`, `base`, `small`, `medium`, `large`）
- `--language`: 言語コード（デフォルト: `en`）

### ステップ4a: 音声クローニング学習（シンプル版）

XTTS-v2のゼロショット音声クローニング（学習不要）：

```bash
cd tts
uv run python train.py
```

オプション:
- `--data`: 学習データディレクトリ（デフォルト: `../data/processed/training`）
- `--output`: モデル出力先（デフォルト: `../data/models/yesman-tts`）
- `--speaker`: 話者名（デフォルト: `yesman`）
- `--language`: 言語コード（デフォルト: `en`）

### ステップ4b: ファインチューニング学習（高品質版・推奨）

XTTS-v2をYes Manの音声でファインチューニング（より高品質）：

```bash
cd tts
uv run python finetune.py
```

オプション:
- `--data`: 学習データディレクトリ（デフォルト: `../data/processed/training`）
- `--output`: モデル出力先（デフォルト: `../data/models/yesman-xtts-finetuned`）
- `--metadata`: メタデータファイル名（デフォルト: `metadata.csv`）
- `--language`: 言語コード（デフォルト: `en`）
- `--batch-size`: バッチサイズ（デフォルト: `4`）
- `--epochs`: エポック数（デフォルト: `100`）
- `--lr`: 学習率（デフォルト: `5e-6`）

**推奨手順**: より高品質な音声合成を実現するには、ステップ4bのファインチューニングを推奨します。

## 学習後の使用方法

学習完了後、以下のコードで音声合成が可能：

```python
from TTS.api import TTS

# モデルのロード
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Yes Manの声で合成
tts.tts_to_file(
    text="Hello! I'm Yes Man!",
    speaker_wav="voice-training/data/models/yesman-tts/yesman_reference.wav",
    language="en",
    file_path="output.wav"
)
```

## ディレクトリ構成

```
voice-training/
├── data/
│   ├── raw/                    # 元の動画ファイル
│   ├── processed/
│   │   ├── extracted/          # 抽出した音声
│   │   └── training/           # 前処理済み音声
│   └── models/
│       └── yesman-tts/         # 学習済みモデル
├── scripts/
│   ├── extract_audio.py        # 動画→音声抽出
│   ├── prepare_data.py         # 音声前処理
│   └── create_metadata.py      # メタデータ生成
├── tts/
│   ├── train.py                # TTS学習（シンプル版）
│   └── finetune.py             # TTSファインチューニング
├── pyproject.toml              # uv依存関係
└── README.md                   # このファイル
```

## トラブルシューティング

### モデルのダウンロードに失敗する
初回実行時、XTTS-v2モデル（約2GB）のダウンロードに時間がかかります。ネットワーク環境を確認してください。

### GPU利用
CUDAが利用可能な場合、自動的にGPUを使用します。CPU学習も可能ですが時間がかかります。

### 音声データが少ない
最低1分、推奨30分以上の音声データが必要です。データが少ないと品質が低下します。

### メモリ不足
大量の音声ファイルを処理する際にメモリ不足になる場合は、バッチ処理を検討してください。
