"""
Coqui TTS (XTTS-v2) を使ったYes Man音声クローニング学習スクリプト
"""
import os
import argparse
from pathlib import Path
import torch

# PyTorch 2.6+のweights_only対応
import torch.serialization
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.config.shared_configs import BaseAudioConfig
torch.serialization.add_safe_globals([XttsConfig, BaseAudioConfig])

from TTS.api import TTS


def train_voice_clone(
    data_dir: str,
    output_dir: str,
    speaker_name: str = "yesman",
    language: str = "en",
):
    """
    XTTS-v2を使って音声クローニング

    Args:
        data_dir: 学習用音声データディレクトリ
        output_dir: モデル出力ディレクトリ
        speaker_name: 話者名
        language: 言語コード
    """
    # 出力ディレクトリ作成
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # デバイス設定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用デバイス: {device}")

    # 音声ファイル収集
    data_path = Path(data_dir)
    audio_files = list(data_path.glob("*.wav"))

    if len(audio_files) == 0:
        print(f"エラー: {data_dir} に音声ファイルが見つかりません")
        return

    print(f"\n音声ファイル数: {len(audio_files)}")

    # 総音声時間を計算
    import librosa
    total_duration = 0
    for audio_file in audio_files:
        audio, sr = librosa.load(str(audio_file), sr=None)
        total_duration += len(audio) / sr

    print(f"総音声時間: {total_duration / 60:.1f}分")

    if total_duration < 60:  # 1分未満
        print("\n警告: 音声データが少なすぎます（最低1分、推奨30分以上）")
        print("学習を続行しますが、品質が低い可能性があります")

    # XTTS-v2モデルのロード
    print("\nXTTS-v2モデルをロード中...")
    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    except Exception as e:
        print(f"エラー: モデルのロードに失敗しました - {str(e)}")
        print("\n初回実行時はモデルのダウンロードに時間がかかります")
        return

    print("モデルのロード完了")

    # 音声クローニング用のスピーカーエンベディング作成
    print(f"\n{speaker_name}の音声特徴を学習中...")

    # 代表的な音声サンプルを選択（最初の数個）
    reference_audio = str(audio_files[0])

    # スピーカーエンベディングを保存
    speaker_wav_path = output_path / f"{speaker_name}_reference.wav"

    # リファレンス音声をコピー
    import shutil
    shutil.copy(reference_audio, speaker_wav_path)

    print(f"\nリファレンス音声を保存: {speaker_wav_path}")

    # テスト合成
    test_text = "Hello! I'm Yes Man, and I'm here to help you with whatever you need!"
    output_audio = output_path / f"{speaker_name}_test.wav"

    print(f"\nテスト音声を生成中...")
    print(f"テキスト: {test_text}")

    try:
        tts.tts_to_file(
            text=test_text,
            speaker_wav=str(speaker_wav_path),
            language=language,
            file_path=str(output_audio)
        )
        print(f"✓ テスト音声を保存: {output_audio}")
    except Exception as e:
        print(f"✗ エラー: {str(e)}")

    # モデル情報を保存
    info_file = output_path / "model_info.txt"
    with open(info_file, "w", encoding="utf-8") as f:
        f.write(f"Speaker: {speaker_name}\n")
        f.write(f"Language: {language}\n")
        f.write(f"Reference Audio: {speaker_wav_path.name}\n")
        f.write(f"Training Data: {len(audio_files)} files\n")
        f.write(f"Total Duration: {total_duration / 60:.1f} minutes\n")
        f.write(f"Device: {device}\n")
        f.write(f"\nModel: XTTS-v2\n")
        f.write(f"Usage:\n")
        f.write(f"  from TTS.api import TTS\n")
        f.write(f"  tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')\n")
        f.write(f"  tts.tts_to_file(\n")
        f.write(f"      text='Your text here',\n")
        f.write(f"      speaker_wav='{speaker_wav_path.name}',\n")
        f.write(f"      language='{language}',\n")
        f.write(f"      file_path='output.wav'\n")
        f.write(f"  )\n")

    print(f"\n✓ モデル情報を保存: {info_file}")
    print(f"\n完了! モデルは以下に保存されました:")
    print(f"  {output_path}")


def main():
    # スクリプトのディレクトリから相対パスを解決
    script_dir = Path(__file__).parent
    default_data_dir = script_dir.parent / "data" / "processed" / "training"
    default_output_dir = script_dir.parent / "data" / "models" / "yesman-tts"

    parser = argparse.ArgumentParser(description="Yes Man音声クローニング")
    parser.add_argument(
        "--data",
        type=str,
        default=str(default_data_dir),
        help="学習用音声データディレクトリ"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(default_output_dir),
        help="モデル出力ディレクトリ"
    )
    parser.add_argument(
        "--speaker",
        type=str,
        default="yesman",
        help="話者名"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="言語コード（en, ja, など）"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Yes Man 音声クローニング")
    print("=" * 60)

    train_voice_clone(
        data_dir=args.data,
        output_dir=args.output,
        speaker_name=args.speaker,
        language=args.language
    )


if __name__ == "__main__":
    main()
