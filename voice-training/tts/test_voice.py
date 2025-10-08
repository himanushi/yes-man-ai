"""
Yes Man音声のテスト合成スクリプト
"""
import argparse


def test_tts(text: str, output_file: str = "test_output.wav", reference_wav: str = "../data/models/yesman-tts/yesman_reference.wav"):
    """
    テキストからYes Manの声で音声合成

    Args:
        text: 合成するテキスト
        output_file: 出力音声ファイル名
        reference_wav: リファレンス音声のパス
    """
    try:
        from TTS.api import TTS
    except ImportError:
        print("エラー: TTS (Coqui TTS) がインストールされていません")
        print("\n以下のコマンドでインストールしてください:")
        print("  pip install TTS")
        return

    print("=" * 60)
    print("Yes Man 音声合成テスト")
    print("=" * 60)
    print(f"\nテキスト: {text}")
    print(f"リファレンス音声: {reference_wav}")
    print(f"出力ファイル: {output_file}")

    print("\nXTTS-v2モデルをロード中...")
    print("（初回実行時は約2GBのモデルダウンロードに時間がかかります）")

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    print("\n音声を合成中...")

    tts.tts_to_file(
        text=text,
        speaker_wav=reference_wav,
        language="en",
        file_path=output_file
    )

    print(f"\n✓ 完了! 音声を保存しました: {output_file}")
    print("\n再生するには:")
    print(f"  start {output_file}  # Windows")
    print(f"  open {output_file}   # Mac")
    print(f"  xdg-open {output_file}  # Linux")


def main():
    parser = argparse.ArgumentParser(description="Yes Man音声合成テスト")
    parser.add_argument(
        "--text",
        type=str,
        default="Hello! I'm Yes Man, and I'm here to help you with whatever you need!",
        help="合成するテキスト"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="test_output.wav",
        help="出力音声ファイル名"
    )
    parser.add_argument(
        "--reference",
        type=str,
        default="../data/models/yesman-tts/yesman_reference.wav",
        help="リファレンス音声のパス"
    )

    args = parser.parse_args()

    test_tts(args.text, args.output, args.reference)


if __name__ == "__main__":
    main()
