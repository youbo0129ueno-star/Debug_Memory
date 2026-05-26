---
id: err_20260526_003
title: ReactでCannot read properties of undefined (reading 'map')
status: resolved
tags:
  - react
  - javascript
  - typescript
language: JavaScript
frameworks:
  - React
created_at: 2026-05-26
updated_at: 2026-05-26
---

## Error

```text
TypeError: Cannot read properties of undefined (reading 'map')
```

## Context

API から取得したデータを `data.map(...)` でレンダリングしたときに発生。初回レンダリング時はまだ fetch が完了しておらず、`data` が `undefined` のため map が呼べない。

## Solution

3つのアプローチがある:

1. **初期値を空配列にする**
   ```javascript
   const [data, setData] = useState([])
   ```

2. **Optional chaining を使う**
   ```javascript
   {data?.map((item) => <Item key={item.id} {...item} />)}
   ```

3. **Loading状態を確認する**
   ```javascript
   if (loading) return <Spinner />
   if (!data) return null
   return data.map(...)
   ```

## Notes

TypeScript を使っているなら `data: Item[] | undefined` のように型を明示すると、コンパイラがガード忘れを検出してくれる。
