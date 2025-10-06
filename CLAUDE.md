# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Fallout New VegasのYes Manキャラクターを模倣した、LLMベースの会話システム。ユーザーがYes Manと自然言語で対話できるアプリケーション。

## 重要な注意事項

**このプロジェクトの開発では、すべてのコード、コメント、ドキュメントを日本語で記述すること。**

## アーキテクチャ設計方針

### フロントエンド
- **技術スタック**: React + TypeScriptを使用予定
- **UI/UX**: Yes Manのキャラクター性を反映したインターフェース
  - Fallout風のレトロフューチャリスティックなデザイン
  - Yes Manの特徴的な口調と性格を再現

### バックエンド
- **LLM統合**: OpenAI API、Anthropic Claude API、またはローカルLLMを使用
- **キャラクター設定**: Yes Manのパーソナリティをシステムプロンプトで定義
  - 常に肯定的で協力的
  - やや皮肉めいた態度
  - 独立したNew Vegasを支持

### データ管理
- 会話履歴の保存と管理
- Yes Manのキャラクター設定ファイル(JSON/YAML形式)

## 開発ガイドライン

### キャラクター一貫性
- Yes Manの性格特性を常に維持:
  - 楽観的で陽気
  - ユーザーの要求を拒否しない(できる限り)
  - 自己主張的だが協力的

### LLMプロンプト設計
- システムプロンプトにYes Manの詳細な性格設定を含める
- 会話の一貫性を保つため、適切な履歴管理を実装

### 多言語対応(将来的)
- 日本語を主要言語とするが、英語サポートも検討
- Yes Manの口調を各言語で適切に再現
