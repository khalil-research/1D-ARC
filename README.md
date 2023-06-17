# 1D-ARC

This repository hosts the 1D-ARC dataset as introduced in the paper: [LLMs and the Abstraction and Reasoning Corpus: Successes, Failures, and the Importance of Object-based Representations.](https://arxiv.org/abs/2305.18354)

See our [project page](https://khalil-research.github.io/LLM4ARC/) for more details.

## Dataset


| Task Name  | 1D-ARC repo dataset        | Visualize                                                                                                 |
| -------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------- |
| Move 1 Pixel               | dataset/1d_move_1p         | ![Alt text](relative%20ds_visualize/Move_1_Pixel.png?raw=true "Move 1 Pixel")                             |
| Move 2 Pixels              | dataset/1d_move_2p         | ![Alt text](relative%20ds_visualize/Move_2_Pixels.png?raw=true "Move 2 Pixels")                           |
| Move 3 Pixels              | dataset/1d_move_3p         | ![Alt text](relative%20ds_visualize/Move_3_Pixels.png?raw=true "Move 3 Pixels")                           |
| Move Dynamic               | dataset/1d_move_dp         | ![Alt text](relative%20ds_visualize/Move_Dynamic.png?raw=true "Move Dynamic")                             |
| Move 2 Pixels Towards      | dataset/1d_move_2p_dp      | ![Alt text](relative%20ds_visualize/Move_2_Pixels_Towards.png?raw=true "Move 2 Pixels Towards")           |
| Fill                       | dataset/1d_fill            | ![Alt text](relative%20ds_visualize/Fill.png?raw=true "Fill")                                             |
| Padded Fill                | dataset/1d_padded_fill     | ![Alt text](relative%20ds_visualize/Padded_Fill.png?raw=true "Padded Fill")                               |
| Hollow                     | dataset/1d_hollow          | ![Alt text](relative%20ds_visualize/Hollow.png?raw=true "Hollow")                                         |
| Flip                       | dataset/1d_flip            | ![Alt text](relative%20ds_visualize/Flip.png?raw=true "Flip")                                             |
| Mirror                     | dataset/1d_mirror          | ![Alt text](relative%20ds_visualize/Mirror.png?raw=true "Mirror")                                         |
| Denoise                    | dataset/1d_denoising_1c    | ![Alt text](relative%20ds_visualize/Denoise.png?raw=true "Denoise")                                       |
| Denoise Multicolor         | dataset/1d_denoising_mc    | ![Alt text](relative%20ds_visualize/Denoise_Multicolor.png?raw=true "Denoise Multicolor")                 |
| Pattern Copy               | dataset/1d_pcopy_1c        | ![Alt text](relative%20ds_visualize/Pattern_Copy.png?raw=true "Pattern Copy")                             |
| Pattern Copy Multicolor    | dataset/1d_pcopy_mc        | ![Alt text](relative%20ds_visualize/Pattern_Copy_Multicolor.png?raw=true "Pattern Copy Multicolor")       |
| Recolor by Odd Even        | dataset/1d_recolor_oe      | ![Alt text](relative%20ds_visualize/Pattern_Copy_Multicolor.png?raw=true "Pattern Copy Multicolor")       |
| Recolor by Size            | dataset/1d_recolor_cnt     | ![Alt text](relative%20ds_visualize/Recolor_by_Size.png?raw=true "Recolor by Size")                       |
| Recolor by Size Comparison | dataset/1d_recolor_cmp     | ![Alt text](relative%20ds_visualize/Recolor_by_Size_Comparison.png?raw=true "Recolor by Size Comparison") |
| Scaling                    | dataset/1d_scale_dp        | ![Alt text](relative%20ds_visualize/Scaling.png?raw=true "Scaling")                                       |
| Lv2 - move and fill        | dataset/1d_lv2_move_n_fill | ![Alt text](relative%20ds_visualize/Lv2MoveFill.png?raw=true "Lv2 move and fill")                         |



## Generators

| 1D-ARC repo dataset        | Generator                            |
| -------------------------- | ------------------------------------ |
| dataset/1d_move_1p         | generator/gen_1d_move.py             |
| dataset/1d_move_2p         | generator/gen_1d_move.py             |
| dataset/1d_move_3p         | generator/gen_1d_move.py             |
| dataset/1d_move_dp         | generator/gen_1d_move.py             |
| dataset/1d_move_2p_dp      | generator/gen_1d_move.py             |
| dataset/1d_fill            | generator/gen_1d_fill.py             |
| dataset/1d_padded_fill     | generator/gen_1d_fill.py             |
| dataset/1d_hollow          | generator/gen_1d_fill.py             |
| dataset/1d_flip            | generator/gen_1d_flip.py             |
| dataset/1d_mirror          | generator/gen_1d_mirror.py           |
| dataset/1d_denoising_1c    | generator/gen_1d_1color_denoising.py |
| dataset/1d_denoising_mc    | generator/gen_1d_mcolor_denoising.py |
| dataset/1d_pcopy_1c        | generator/gen_1d_pattern_copy.py     |
| dataset/1d_pcopy_mc        | generator/gen_1d_pattern_copy.py     |
| dataset/1d_recolor_oe      | generator/gen_1d_recolor.py          |
| dataset/1d_recolor_cnt     | generator/gen_1d_recolor.py          |
| dataset/1d_recolor_cmp     | generator/gen_1d_recolor.py          |
| dataset/1d_scale_dp        | generator/gen_1d_move.py             |
| dataset/1d_lv2_move_n_fill | generator/gen_1d_lv2.py              |

