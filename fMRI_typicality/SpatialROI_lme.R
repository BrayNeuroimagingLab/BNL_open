library(lme4)
library(lmerTest)
library(psych)

spatialROI_pairs <- read.csv('/Users/.../spatialROI_pairs_dice.csv')
spatialROI_pairs$Subj1 <- as.factor(spatialROI_pairs$Subj1)
spatialROI_pairs$Subj2 <- as.factor(spatialROI_pairs$Subj2)
spatialROI_pairs$PairSex <- as.factor(spatialROI_pairs$PairSex)

# LMEs for the logit transformed Dice coefficient
# Delete the -Inf and Inf
pairs_noinf_rhFFA_p005 <- spatialROI_pairs[is.finite(spatialROI_pairs$rhFFA_dice_p005_logit), ]
pairs_noinf_lhFFA_p005 <- spatialROI_pairs[is.finite(spatialROI_pairs$lhFFA_dice_p005_logit), ]
pairs_noinf_rhSTS_p005 <- spatialROI_pairs[is.finite(spatialROI_pairs$rhSTS_dice_p005_logit), ]
pairs_noinf_lhSTS_p005 <- spatialROI_pairs[is.finite(spatialROI_pairs$lhSTS_dice_p005_logit), ]

# LMEs
rhFFA_dsc_logit_p005_lme <- summary(lmer(rhFFA_dice_p005_logit ~ 0 + AvgAge + AgeDiff + TotCenVol + PairSex + (1|Subj1) + (1|Subj2), data = pairs_noinf_rhFFA_p005))
lhFFA_dsc_logit_p005_lme <- summary(lmer(lhFFA_dice_p005_logit ~ 0 + AvgAge + AgeDiff + TotCenVol + PairSex + (1|Subj1) + (1|Subj2), data = pairs_noinf_lhFFA_p005))
rhSTS_dsc_logit_p005_lme <- summary(lmer(rhSTS_dice_p005_logit ~ 0 + AvgAge + AgeDiff + TotCenVol + PairSex + (1|Subj1) + (1|Subj2), data = pairs_noinf_rhSTS_p005))
lhSTS_dsc_logit_p005_lme <- summary(lmer(lhSTS_dice_p005_logit ~ 0 + AvgAge + AgeDiff + TotCenVol + PairSex + (1|Subj1) + (1|Subj2), data = pairs_noinf_lhSTS_p005))

# Multiple comparisons
p.adjust(c(0.3662, 0.6628, 0.00137, 0.05809, 0.874911, 0.423091, 0.35134, 0.83269), method = "fdr")
# [1] 0.6769456 0.8749110 0.0109600 0.2323600 0.8749110 0.6769456 0.6769456 0.8749110


