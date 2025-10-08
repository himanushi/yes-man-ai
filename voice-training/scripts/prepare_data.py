"""
音声データの前処理スクリプト
- 無音区間の除去
- 音量正規化
- ノイズ除去
- セグメント分割
"""
import os
import argparse
from pathlib import Path
import librosa
import soundfile as sf
import numpy as np
from tqdm import tqdm


def trim_silence(audio: np.ndarray, sr: int, threshold_db: float = 30) -> np.ndarray:
    """
    音声の前後の無音区間を除去

    Args:
        audio: 音声データ
        sr: サンプリングレート
        threshold_db: 無音判定の閾値（dB）

    Returns:
        トリミング後の音声データ
    """
    trimmed, _ = librosa.effects.trim(audio, top_db=threshold_db)
    return trimmed


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    """
    音声を正規化（最大振幅を-1.0〜1.0に調整）

    Args:
        audio: 音声データ

    Returns:
        正規化後の音声データ
    """
    max_val = np.abs(audio).max()
    if max_val > 0:
        return audio / max_val * 0.95  # 0.95倍でクリッピング防止
    return audio


def reduce_noise(audio: np.ndarray, sr: int) -> np.ndarray:
    """
    簡易ノイズ除去（ハイパスフィルタ）

    Args:
        audio: 音声データ
        sr: サンプリングレート

    Returns:
        ノイズ除去後の音声データ
    """
    # 80Hz以下をカット（低周波ノイズ除去）
    audio_filtered = librosa.effects.preemphasis(audio)
    return audio_filtered


def split_audio(audio: np.ndarray, sr: int, max_duration: float = 10.0, min_duration: float = 1.0):
    """
    音声を一定長のセグメントに分割

    Args:
        audio: 音声データ
        sr: サンプリングレート
        max_duration: 最大セグメント長（秒）
        min_duration: 最小セグメント長（秒）

    Yields:
        分割された音声セグメント
    """
    # 無音区間で分割
    intervals = librosa.effects.split(audio, top_db=30)

    for start, end in intervals:
        segment = audio[start:end]
        duration = len(segment) / sr

        # 最小長チェック
        if duration < min_duration:
            continue

        # 最大長を超える場合は分割
        if duration > max_duration:
            max_samples = int(max_duration * sr)
            for i in range(0, len(segment), max_samples):
                chunk = segment[i:i + max_samples]
                if len(chunk) / sr >= min_duration:
                    yield chunk
        else:
            yield segment


def process_audio_file(input_path: str, output_dir: str, sr: int = 16000):
    """
    1つの音声ファイルを処理

    Args:
        input_path: 入力音声ファイル
        output_dir: 出力ディレクトリ
        sr: 目標サンプリングレート
    """
    try:
        # 音声読み込み
        audio, original_sr = librosa.load(input_path, sr=sr, mono=True)

        # 前処理
        audio = trim_silence(audio, sr)
        audio = normalize_audio(audio)
        audio = reduce_noise(audio, sr)

        # セグメント分割
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        input_filename = Path(input_path).stem
        segments = list(split_audio(audio, sr))

        if not segments:
            print(f"  警告: {input_path} からセグメントを抽出できませんでした")
            return 0

        # 各セグメントを保存
        for i, segment in enumerate(segments):
            output_file = output_path / f"{input_filename}_seg{i:03d}.wav"
            sf.write(output_file, segment, sr)

        print(f"  ✓ {input_filename}: {len(segments)}セグメント生成")
        return len(segments)

    except Exception as e:
        print(f"  ✗ エラー: {input_path} - {str(e)}")
        return 0


def process_directory(input_dir: str, output_dir: str, sr: int = 16000):
    """
    ディレクトリ内の全音声ファイルを処理

    Args:
        input_dir: 入力ディレクトリ
        output_dir: 出力ディレクトリ
        sr: 目標サンプリングレート
    """
    input_path = Path(input_dir)

    # 音声ファイルを検索
    audio_extensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(input_path.glob(f"*{ext}"))
        audio_files.extend(input_path.glob(f"*{ext.upper()}"))

    if not audio_files:
        print(f"警告: {input_dir} に音声ファイルが見つかりません")
        return

    print(f"\n{len(audio_files)}個の音声ファイルが見つかりました\n")

    # 各音声ファイルを処理
    total_segments = 0
    for audio_file in tqdm(audio_files, desc="音声処理中"):
        segments = process_audio_file(str(audio_file), output_dir, sr)
        total_segments += segments

    print(f"\n完了: 合計 {total_segments} セグメントを生成しました")
    print(f"出力先: {output_dir}")


def main():
    # スクリプトのディレクトリから相対パスを解決
    script_dir = Path(__file__).parent
    default_input_dir = script_dir.parent / "data" / "processed" / "extracted"
    default_output_dir = script_dir.parent / "data" / "processed" / "training"

    parser = argparse.ArgumentParser(description="音声データを前処理")
    parser.add_argument(
        "--input",
        type=str,
        default=str(default_input_dir),
        help="入力ディレクトリ（抽出済み音声ファイル）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(default_output_dir),
        help="出力ディレクトリ（学習用音声ファイル）"
    )
    parser.add_argument(
        "--sr",
        type=int,
        default=16000,
        help="サンプリングレート（Hz）"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Yes Man 音声前処理ツール")
    print("=" * 60)

    process_directory(args.input, args.output, args.sr)


if __name__ == "__main__":
    main()
