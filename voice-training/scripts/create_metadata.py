"""
音声ファイルに対応するメタデータ（transcript）を生成するスクリプト
Whisperを使って自動文字起こしを行い、metadata.csvを生成
"""
import os
import argparse
from pathlib import Path
import csv
from tqdm import tqdm
import whisper
import torch


def transcribe_audio_files(
    audio_dir: str,
    output_csv: str,
    model_size: str = "base",
    language: str = "en"
):
    """
    音声ファイルを文字起こしし、metadata.csvを生成

    Args:
        audio_dir: 音声ファイルが格納されたディレクトリ
        output_csv: 出力するmetadata.csvのパス
        model_size: Whisperモデルのサイズ (tiny, base, small, medium, large)
        language: 言語コード (en, ja など)
    """
    # デバイス設定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用デバイス: {device}")

    # Whisperモデルのロード
    print(f"\nWhisper {model_size} モデルをロード中...")
    model = whisper.load_model(model_size, device=device)
    print("モデルのロード完了")

    # 音声ファイルを取得
    audio_path = Path(audio_dir)
    audio_files = sorted(audio_path.glob("*.wav"))

    if not audio_files:
        print(f"エラー: {audio_dir} に音声ファイルが見つかりません")
        return

    print(f"\n{len(audio_files)}個の音声ファイルが見つかりました\n")

    # メタデータリスト
    metadata = []

    # 各音声ファイルを文字起こし
    for audio_file in tqdm(audio_files, desc="文字起こし中"):
        try:
            # Whisperで文字起こし
            result = model.transcribe(
                str(audio_file),
                language=language,
                fp16=(device == "cuda")
            )

            text = result["text"].strip()

            # メタデータに追加 (ファイル名|テキスト形式)
            metadata.append({
                "audio_file": audio_file.name,
                "text": text
            })

        except Exception as e:
            print(f"\n警告: {audio_file.name} の処理中にエラー - {str(e)}")
            continue

    # CSVファイルに書き出し
    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["audio_file", "text"], delimiter="|")
        for row in metadata:
            f.write(f"{row['audio_file']}|{row['text']}\n")

    print(f"\n✓ メタデータを保存: {output_csv}")
    print(f"  総ファイル数: {len(metadata)}")

    # サンプル表示
    print("\n--- サンプル (最初の5件) ---")
    for i, row in enumerate(metadata[:5]):
        print(f"{i+1}. {row['audio_file']}")
        print(f"   テキスト: {row['text']}\n")


def main():
    # スクリプトのディレクトリから相対パスを解決
    script_dir = Path(__file__).parent
    default_audio_dir = script_dir.parent / "data" / "processed" / "training"
    default_output = default_audio_dir / "metadata.csv"

    parser = argparse.ArgumentParser(description="音声ファイルからメタデータを生成")
    parser.add_argument(
        "--audio",
        type=str,
        default=str(default_audio_dir),
        help="音声ファイルディレクトリ"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(default_output),
        help="出力するmetadata.csvのパス"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisperモデルのサイズ"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="言語コード (en, ja など)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("音声メタデータ生成ツール")
    print("=" * 60)

    transcribe_audio_files(
        audio_dir=args.audio,
        output_csv=args.output,
        model_size=args.model,
        language=args.language
    )


if __name__ == "__main__":
    main()
