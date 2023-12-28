# VMatrix Core Images

Create VMatrix core images.

## The Pipelines

1. Extract skill icons from `Skill.wz` to `./img/skills` using [WzComparerR2](https://github.com/KENNYSOFT/WzComparerR2).
   - Check all skill icons are (32,32,4).
2. Extract the background, frame, mask, lock icons from `UI.wz/VMatrixUI.img` to `./img/VMatrixUI`.

   ![Picture of frame](./img/VMatrixUI/VMatrix.SlotState.Equip_ENCore.png)
   ![Picture of frame](./img/VMatrixUI/VMatrix.iconFrame.frame3.png)
   ![Picture of frame](./img/VMatrixUI/VMatrix.iconMask.3A_32.png)
   ![Picture of frame](./img/VMatrixUI/VMatrix.iconMask.3B_32.png)
   ![Picture of frame](./img/VMatrixUI/VMatrix.ProtectLock.0.png)

3. Mask skill icons for each directions.

   ![Picture of icon](./img/skills/Adele/Cleave.png)
   →
   ![Picture of left mask icon](./img/skills/Adele/left/Cleave.png)
   ![Picture of right mask icon](./img/skills/Adele/right/Cleave.png)
   ![Picture of up mask icon](./img/skills/Adele/up/Cleave.png)
4. Merge three masked skill icons. (left+right+up, 3-permutations)

   ![Picture of icon 1](./img/skills/Adele/left/Cleave.png)
   +
   ![Picture of icon 2](./img/skills/Adele/right/Eviscerate.png)
   +
   ![Picture of icon 3](./img/skills/Adele/up/Skewering.png)
   →
   ![Picture of combination](./img/skills/Adele/comb/Cleave+Eviscerate+Skewering.png)
5. Add frame to merged images.

   ![Picture of combination](./img/skills/Adele/comb/Cleave+Eviscerate+Skewering.png)
   +
   ![Picture of frame](./img/VMatrixUI/VMatrix.iconFrame.frame3.png)
   →
   ![Picture of combination](./img/skills/Adele/comb+frame/Cleave+Eviscerate+Skewering.png)
6. Add lock to merged images.

   ![Picture of combination](./img/skills/Adele/comb+frame/Cleave+Eviscerate+Skewering.png)
   +
   ![Picture of lock](./img/VMatrixUI/VMatrix.ProtectLock.0.png)
   →
   ![Picture of combination](./img/skills/Adele/comb+frame+lock/Cleave+Eviscerate+Skewering.png)


### Image File Structures

```tree
img
├─VMatrixUI
└─skills
   ├─Adele
   │  ├─comb+frame
   │  │  ├─Cleave+Eviscerate+Skewering.png
   │  │  ├─Cleave+Skewering+Eviscerate.png
   │  │  ├─Eviscerate+Cleave+Skewering.png
   │  │  └─ ...
   │  ├─comb+frame+lock
   │  │  ├─Cleave+Eviscerate+Skewering.png
   │  │  ├─Cleave+Skewering+Eviscerate.png
   │  │  ├─Eviscerate+Cleave+Skewering.png
   │  │  └─ ...
   │  ├─Cleave.png
   │  ├─Eviscerate.png
   │  └─ ...
   └─ ...
```

## TODO

- [ ] imagesearch from in-game screenshots
- [ ] find the valid combinations
