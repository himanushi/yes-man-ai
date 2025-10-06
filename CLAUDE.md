# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Yes Manの陽気で明るい性格を持つ、LLMベースの音声会話アシスタントシステム。ユーザーと自然言語で対話できるアプリケーション。

### 主要機能

1. **音声会話**
   - Yes Manの声で応答（音声合成）
   - ウェイクアップワード不要：常時音声を聞き取り、質問されていると判断したら自動的に応答
   - 連続的な会話フローをサポート

2. **Agent機能**
   - Web検索機能
   - Apple Music再生制御（MusicKit.js使用）
   - その他の拡張可能なツール統合

3. **キャラクター性**
   - 陽気で明るく、常にポジティブな態度
   - エネルギッシュで親しみやすい口調
   - ユーザーを励まし、サポートする姿勢

## 重要な注意事項

**このプロジェクトの開発では、すべてのコード、コメント、ドキュメントを日本語で記述すること。**

## プロジェクト構成

```
yes-man-ai/
├── frontend/          # React + TypeScript フロントエンド
└── backend/           # Python (FastAPI) バックエンド
```

## アーキテクチャ設計方針

### フロントエンド (React + TypeScript)
- **ディレクトリ**: `frontend/`
- **技術スタック**: React + TypeScript + Vite
- **音声処理**:
  - Web Speech API (音声認識)
  - Web Audio API または Speech Synthesis API (音声合成)
  - 常時音声モニタリング機能
- **音楽統合**:
  - MusicKit.js (Apple Music再生制御)
- **UI/UX**: Yes Manのキャラクター性を反映したインターフェース
  - 明るく親しみやすいデザイン
  - 音声波形や会話状態の可視化
- **状態管理**: React Context API または Zustand
- **スタイリング**: CSS Modules または Tailwind CSS

### バックエンド (Python + FastAPI)
- **ディレクトリ**: `backend/`
- **技術スタック**: Python 3.11+, FastAPI, uvicorn
- **LLM統合**:
  - OpenAI API、Anthropic Claude API、またはローカルLLM
  - Function Calling / Tool Use機能を活用
- **音声処理**:
  - 音声合成 (TTS): ElevenLabs、OpenAI TTS、またはオープンソースTTS
  - Yes Manの声を再現
- **Agent機能**:
  - Web検索ツール (Google Search API、SerpAPIなど)
  - Apple Music制御用APIエンドポイント
  - ツールの動的実行フレームワーク
- **会話判定ロジック**:
  - 音声入力テキストから質問意図を検出
  - 応答すべきタイミングを判断するロジック
- **API設計**: RESTful + WebSocket
  - `/api/chat` - 会話エンドポイント
  - `/api/voice/synthesize` - 音声合成
  - `/ws/conversation` - リアルタイム会話用WebSocket
  - `/api/history` - 会話履歴の取得・保存
- **キャラクター設定**: Yes Manのパーソナリティをシステムプロンプトで定義
  - 常に肯定的で協力的
  - 陽気で明るく、エネルギッシュ
  - ユーザーのリクエストを喜んで受け入れる

### データ管理
- 会話履歴の保存と管理 (SQLite または JSON ファイル)
- Yes Manのキャラクター設定ファイル(YAML形式: `backend/config/yesman_personality.yaml`)

## 開発ガイドライン

### キャラクター一貫性
- Yes Manの性格特性を常に維持:
  - 楽観的で陽気、常に明るい
  - ポジティブでエネルギッシュな態度
  - ユーザーの要求を喜んで受け入れる
  - 親しみやすく、フレンドリーな口調

### LLMプロンプト設計
- システムプロンプトにYes Manの詳細な性格設定を含める
- 会話の一貫性を保つため、適切な履歴管理を実装
- 質問検出プロンプト：ユーザーの発言が質問か独り言かを判定

### 音声インタラクション設計
- **常時リスニング**: バックグラウンドで常に音声を監視
- **質問検出**: LLMが発言内容から質問意図を判断
- **自然な応答タイミング**: 質問と判定された場合のみ応答
- **音声合成**: Yes Manの特徴的な声で回答

### Agent Tool設計
- **検索機能**: Web検索を実行し、結果を要約してYes Man風に回答
- **Apple Music制御**:
  - MusicKit.js経由で楽曲検索・再生・停止・スキップ
  - プレイリスト管理
  - 現在再生中の曲情報取得
- **拡張性**: 新しいツールを簡単に追加できる設計

### 多言語対応(将来的)
- 日本語を主要言語とするが、英語サポートも検討
- Yes Manの口調を各言語で適切に再現
