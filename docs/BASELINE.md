# Source baseline and scope

Version 1.0.2 was staged independently from the clean local Foods repository at commit `5938b8d738955cd42ab4ee4b3106a2f17e4db50b` (published v1.0.1). Development used a separate staging area. No original-repository changes, installed-mod writes, game lifecycle actions or save/settings access were performed. Publication was separately authorized after implementation; a separate publishing checkout preserves the original repository. No applicable local AGENTS.md was found in the inspected repository or workspace ancestry. Concurrent Animals development was not accessed or changed.

The existing cheese recipe and shared heat helper retain their exact original bytes:

| File | SHA-256 |
| --- | --- |
| `EwingsFoods/42/media/scripts/ewingsfoods_cheese.txt` | `a30c8a1bcab17ac23a2b8d00eea4faae267e1db64028ecadaf2afd01abd69999` |
| `EwingsFoods/42/media/lua/shared/EwingsFoodsHeat.lua` | `b0687ca6f5a3a7f946210a2e72f1ac6538ef9851c3c9575f3cf6e0c4b32578d0` |

The update adds the tomato recipe and a small shared OnTest predicate; metadata, English translations, documentation, focused validation and packaging tools are updated. No installed vanilla item definition is overridden. The same mod ID and 42.21 bounds remain.

## 1.1.0 nachos staging

Staged independently from published 1.0.2 commit `8787adb1f267b0d787f36bc676f83122650ab04a`. Existing cheese recipe, heat helper, tomato recipe and tomato predicate remain byte-identical. Development changed only the isolated 1.1.0 stage and preserved the original repository and installed Foods 1.0.1. Publication and guarded local installation were subsequently authorized separately; the publishing checkout contains only the reviewed release changes. Installation must back up and verify the existing mod, then recheck that game/server processes are closed before replacing only EwingsFoods. It adds one custom saved item; see NACHOS.md for removal limitations.
