"""
XTTS-v2モデルのファインチューニングスクリプト
Yes Manの音声データでモデルを微調整
"""
import os
import argparse
from pathlib import Path
import torch

# PyTorch 2.6+のweights_only対応
import torch.serialization
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.config.shared_configs import BaseDatasetConfig, BaseAudioConfig
torch.serialization.add_safe_globals([XttsConfig, BaseDatasetConfig, BaseAudioConfig])

from trainer import Trainer, TrainerArgs
from TTS.tts.models.xtts import Xtts
from TTS.tts.datasets import load_tts_samples


def setup_dataset_config(data_dir: str, metadata_file: str, language: str = "en"):
    """
    データセット設定を作成

    Args:
        data_dir: 音声データディレクトリ
        metadata_file: メタデータファイル（metadata.csv）
        language: 言語コード

    Returns:
        データセット設定
    """
    dataset_config = BaseDatasetConfig(
        formatter="ljspeech",  # フォーマッタ (カスタム可能)
        meta_file_train=metadata_file,
        path=data_dir,
        language=language,
    )
    return dataset_config


def finetune_xtts(
    data_dir: str,
    output_dir: str,
    metadata_file: str = "metadata.csv",
    language: str = "en",
    batch_size: int = 4,
    epochs: int = 100,
    learning_rate: float = 5e-6,
):
    """
    XTTS-v2をファインチューニング

    Args:
        data_dir: 学習用音声データディレクトリ
        output_dir: モデル出力ディレクトリ
        metadata_file: メタデータファイル名
        language: 言語コード
        batch_size: バッチサイズ
        epochs: エポック数
        learning_rate: 学習率
    """
    # 出力ディレクトリ作成
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # デバイス設定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用デバイス: {device}")

    # メタデータファイルのパス
    metadata_path = Path(data_dir) / metadata_file
    if not metadata_path.exists():
        print(f"エラー: メタデータファイルが見つかりません: {metadata_path}")
        print("まず create_metadata.py を実行してください")
        return

    print(f"メタデータファイル: {metadata_path}")

    # データセット設定
    dataset_config = setup_dataset_config(
        data_dir=data_dir,
        metadata_file=str(metadata_path),
        language=language
    )

    # XTTS設定
    config = XttsConfig()
    config.load_json("tts_models/multilingual/multi-dataset/xtts_v2/config.json")

    # 学習パラメータの設定
    config.batch_size = batch_size
    config.num_loader_workers = 4
    config.datasets = [dataset_config]
    config.output_path = str(output_path)

    # モデルのロード
    print("\nXTTS-v2モデルをロード中...")
    model = Xtts.init_from_config(config)
    model.load_checkpoint(
        config,
        checkpoint_dir="tts_models/multilingual/multi-dataset/xtts_v2/",
        eval=False
    )

    # データセットのロード
    train_samples, eval_samples = load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_size=0.1
    )

    print(f"\n学習サンプル数: {len(train_samples)}")
    print(f"検証サンプル数: {len(eval_samples)}")

    # Trainerの設定
    trainer_args = TrainerArgs(
        restore_path=None,
        skip_train_epoch=False,
        start_with_eval=True,
        grad_accum_steps=1,
    )

    trainer = Trainer(
        trainer_args,
        config,
        output_path=str(output_path),
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
    )

    print("\n学習を開始します...")
    print(f"エポック数: {epochs}")
    print(f"バッチサイズ: {batch_size}")
    print(f"学習率: {learning_rate}\n")

    # 学習実行
    trainer.fit()

    print(f"\n✓ 学習完了")
    print(f"モデル保存先: {output_path}")


def main():
    # スクリプトのディレクトリから相対パスを解決
    script_dir = Path(__file__).parent
    default_data_dir = script_dir.parent / "data" / "processed" / "training"
    default_output_dir = script_dir.parent / "data" / "models" / "yesman-xtts-finetuned"

    parser = argparse.ArgumentParser(description="XTTS-v2ファインチューニング")
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
        "--metadata",
        type=str,
        default="metadata.csv",
        help="メタデータファイル名"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="言語コード"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="バッチサイズ"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="エポック数"
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=5e-6,
        help="学習率"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Yes Man XTTS-v2 ファインチューニング")
    print("=" * 60)

    finetune_xtts(
        data_dir=args.data,
        output_dir=args.output,
        metadata_file=args.metadata,
        language=args.language,
        batch_size=args.batch_size,
        epochs=args.epochs,
        learning_rate=args.lr,
    )


if __name__ == "__main__":
    main()
