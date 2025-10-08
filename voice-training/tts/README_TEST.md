# Yes Man 音声テスト方法

## WindowsでのTTSインストール

Windows環境では、TTSのビルドにVisual C++が必要ですが、以下の回避策があります：

### 方法1: 別の環境でテスト（推奨）

バックエンドで使用する際にインストールします。今はリファレンス音声の準備が完了しているので、バックエンド実装時にテストできます。

### 方法2: Google Colabでテスト

以下のコードをGoogle Colabで実行：

```python
# パッケージインストール
!pip install TTS

# リファレンス音声をアップロード（Google Colabのファイルアップロード機能を使用）
# yesman_reference.wav をアップロード

# テスト実行
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

tts.tts_to_file(
    text="Hello! I'm Yes Man, and I'm here to help you!",
    speaker_wav="yesman_reference.wav",
    language="en",
    file_path="output.wav"
)

# 再生
from IPython.display import Audio
Audio("output.wav")
```

### 方法3: WSL2 (Windows Subsystem for Linux) でテスト

WSL2がインストール済みの場合：

```bash
# WSL2で実行
wsl
cd /mnt/c/Users/ma5an/Work/yes-man-ai/voice-training
pip install TTS
python tts/test_voice.py --text "Hello! I'm Yes Man!"
```

## リファレンス音声の場所

準備完了した音声ファイル：
- `voice-training/data/models/yesman-tts/yesman_reference.wav`

このファイルをバックエンドで使用してYes Manの声を再現できます。
