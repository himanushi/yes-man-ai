"""
シンプルなYes Man音声クローニング（リファレンス音声保存）
Coqui TTSのビルド問題を回避し、推論時にXTTS-v2を使用
"""
import os
import argparse
from pathlib import Path
import shutil
import librosa


def prepare_voice_clone(
    data_dir: str,
    output_dir: str,
    speaker_name: str = "yesman",
):
    """
    音声クローニング用のリファレンス音声を準備

    Args:
        data_dir: 学習用音声データディレクトリ
        output_dir: モデル出力ディレクトリ
        speaker_name: 話者名
    """
    # 出力ディレクトリ作成
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 音声ファイル収集
    data_path = Path(data_dir)
    audio_files = list(data_path.glob("*.wav"))

    if len(audio_files) == 0:
        print(f"エラー: {data_dir} に音声ファイルが見つかりません")
        return

    print(f"\n音声ファイル数: {len(audio_files)}")

    # 総音声時間を計算
    total_duration = 0
    audio_durations = []

    for audio_file in audio_files:
        audio, sr = librosa.load(str(audio_file), sr=None)
        duration = len(audio) / sr
        total_duration += duration
        audio_durations.append((audio_file, duration))

    print(f"総音声時間: {total_duration / 60:.1f}分")

    if total_duration < 60:  # 1分未満
        print("\n警告: 音声データが少なすぎます（最低1分、推奨30分以上）")

    # 最も長い音声をリファレンスとして選択
    audio_durations.sort(key=lambda x: x[1], reverse=True)
    reference_audio = audio_durations[0][0]

    print(f"\nリファレンス音声: {reference_audio.name} ({audio_durations[0][1]:.1f}秒)")

    # リファレンス音声をコピー
    speaker_wav_path = output_path / f"{speaker_name}_reference.wav"
    shutil.copy(reference_audio, speaker_wav_path)

    print(f"リファレンス音声を保存: {speaker_wav_path}")

    # 追加の音声サンプルもコピー（最大5個）
    samples_dir = output_path / "samples"
    samples_dir.mkdir(exist_ok=True)

    for i, (audio_file, duration) in enumerate(audio_durations[:5]):
        sample_path = samples_dir / f"sample_{i:02d}.wav"
        shutil.copy(audio_file, sample_path)
        print(f"サンプル音声{i+1}を保存: {sample_path}")

    # 使用方法を保存
    readme_file = output_path / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(f"# Yes Man 音声モデル\n\n")
        f.write(f"## 情報\n\n")
        f.write(f"- **話者**: {speaker_name}\n")
        f.write(f"- **リファレンス音声**: {speaker_wav_path.name}\n")
        f.write(f"- **学習データ**: {len(audio_files)} ファイル\n")
        f.write(f"- **総音声時間**: {total_duration / 60:.1f} 分\n\n")
        f.write(f"## バックエンドでの使用方法\n\n")
        f.write(f"### 1. Coqui TTSをインストール\n\n")
        f.write(f"```bash\n")
        f.write(f"pip install TTS\n")
        f.write(f"```\n\n")
        f.write(f"### 2. Pythonコード例\n\n")
        f.write(f"```python\n")
        f.write(f"from TTS.api import TTS\n\n")
        f.write(f"# モデルのロード（初回のみダウンロード）\n")
        f.write(f"tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')\n\n")
        f.write(f"# Yes Manの声で音声合成\n")
        f.write(f"tts.tts_to_file(\n")
        f.write(f"    text='Hello! I\\'m Yes Man, and I\\'m here to help!',\n")
        f.write(f"    speaker_wav='{speaker_wav_path}',\n")
        f.write(f"    language='en',\n")
        f.write(f"    file_path='output.wav'\n")
        f.write(f")\n")
        f.write(f"```\n\n")
        f.write(f"### 3. このディレクトリをバックエンドにコピー\n\n")
        f.write(f"```bash\n")
        f.write(f"cp -r {output_path} ../../backend/models/\n")
        f.write(f"```\n\n")
        f.write(f"## テスト\n\n")
        f.write(f"以下のコマンドでテスト合成を実行できます：\n\n")
        f.write(f"```bash\n")
        f.write(f"python test_tts.py\n")
        f.write(f"```\n")

    print(f"\n✓ README を保存: {readme_file}")

    # テストスクリプトも作成
    test_script = output_path / "test_tts.py"
    with open(test_script, "w", encoding="utf-8") as f:
        f.write(f"from TTS.api import TTS\n\n")
        f.write(f"print('XTTS-v2モデルをロード中...')\n")
        f.write(f"tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')\n\n")
        f.write(f"print('音声を合成中...')\n")
        f.write(f"tts.tts_to_file(\n")
        f.write(f"    text='Hello! I am Yes Man! How can I help you today?',\n")
        f.write(f"    speaker_wav='{speaker_wav_path.name}',\n")
        f.write(f"    language='en',\n")
        f.write(f"    file_path='test_output.wav'\n")
        f.write(f")\n\n")
        f.write(f"print('完了: test_output.wav')\n")

    print(f"✓ テストスクリプトを保存: {test_script}")
    print(f"\n完了! モデルは以下に保存されました:")
    print(f"  {output_path}")
    print(f"\nバックエンドで使用するには、このディレクトリを backend/models/ にコピーしてください")


def main():
    parser = argparse.ArgumentParser(description="Yes Man音声クローニング（シンプル版）")
    parser.add_argument(
        "--data",
        type=str,
        default="../data/processed/training",
        help="学習用音声データディレクトリ"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../data/models/yesman-tts",
        help="モデル出力ディレクトリ"
    )
    parser.add_argument(
        "--speaker",
        type=str,
        default="yesman",
        help="話者名"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Yes Man 音声クローニング（シンプル版）")
    print("=" * 60)

    prepare_voice_clone(
        data_dir=args.data,
        output_dir=args.output,
        speaker_name=args.speaker
    )


if __name__ == "__main__":
    main()
