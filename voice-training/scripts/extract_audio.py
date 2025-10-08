"""
動画ファイルから音声を抽出するスクリプト
"""
import os
import argparse
from pathlib import Path
try:
    from moviepy import VideoFileClip
except ImportError:
    from moviepy.editor import VideoFileClip
from tqdm import tqdm


def extract_audio_from_video(video_path: str, output_path: str, audio_format: str = "wav"):
    """
    動画ファイルから音声を抽出

    Args:
        video_path: 入力動画ファイルのパス
        output_path: 出力音声ファイルのパス
        audio_format: 出力形式 (wav, mp3など)
    """
    try:
        print(f"動画を読み込み中: {video_path}")
        video = VideoFileClip(video_path)

        print(f"音声を抽出中...")
        audio = video.audio

        print(f"音声を保存中: {output_path}")
        audio.write_audiofile(
            output_path,
            codec='pcm_s16le' if audio_format == 'wav' else None,
            fps=16000,  # 16kHzサンプリングレート（音声学習に適している）
            nbytes=2,
            bitrate="128k"
        )

        # リソース解放
        audio.close()
        video.close()

        print(f"✓ 完了: {output_path}")
        return True

    except Exception as e:
        print(f"✗ エラー: {video_path} - {str(e)}")
        return False


def process_directory(input_dir: str, output_dir: str, audio_format: str = "wav"):
    """
    ディレクトリ内の全ての動画ファイルを処理

    Args:
        input_dir: 入力ディレクトリ
        output_dir: 出力ディレクトリ
        audio_format: 出力形式
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # サポートする動画形式
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

    # 動画ファイルを検索
    video_files = []
    for ext in video_extensions:
        video_files.extend(input_path.glob(f"*{ext}"))
        video_files.extend(input_path.glob(f"*{ext.upper()}"))

    if not video_files:
        print(f"警告: {input_dir} に動画ファイルが見つかりません")
        return

    print(f"\n{len(video_files)}個の動画ファイルが見つかりました\n")

    # 各動画ファイルを処理
    success_count = 0
    for video_file in tqdm(video_files, desc="音声抽出中"):
        output_file = output_path / f"{video_file.stem}.{audio_format}"

        if extract_audio_from_video(str(video_file), str(output_file), audio_format):
            success_count += 1

    print(f"\n完了: {success_count}/{len(video_files)} ファイルを処理しました")


def main():
    # スクリプトのディレクトリから相対パスを解決
    script_dir = Path(__file__).parent
    default_input_dir = script_dir.parent / "data" / "raw"
    default_output_dir = script_dir.parent / "data" / "processed" / "extracted"

    parser = argparse.ArgumentParser(description="動画から音声を抽出")
    parser.add_argument(
        "--input",
        type=str,
        default=str(default_input_dir),
        help="入力ディレクトリ（動画ファイルが格納されている）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(default_output_dir),
        help="出力ディレクトリ（音声ファイルを保存）"
    )
    parser.add_argument(
        "--format",
        type=str,
        default="wav",
        choices=["wav", "mp3"],
        help="出力音声形式"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Yes Man 音声抽出ツール")
    print("=" * 60)

    process_directory(args.input, args.output, args.format)


if __name__ == "__main__":
    main()
