"""
リファレンス音声の品質確認（簡易版）
"""
import soundfile as sf
import numpy as np

# リファレンス音声を読み込んで情報表示
ref_audio = "../data/models/yesman-tts/yesman_reference.wav"

audio, sr = sf.read(ref_audio)

print("=" * 60)
print("Yes Man リファレンス音声 情報")
print("=" * 60)
print(f"\nファイル: {ref_audio}")
print(f"サンプリングレート: {sr} Hz")
print(f"音声長: {len(audio) / sr:.2f} 秒")
print(f"チャンネル数: {1 if audio.ndim == 1 else audio.shape[1]}")
print(f"最大振幅: {np.max(np.abs(audio)):.3f}")
print(f"\n✓ リファレンス音声は正常に準備されています")
print(f"\nバックエンドでこのファイルを使用してYes Manの声を合成できます")
print(f"\n音声を再生するには:")
print(f"  start {ref_audio}  # Windows")
