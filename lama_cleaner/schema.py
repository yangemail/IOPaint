from enum import Enum
from typing import Optional

from PIL.Image import Image
from pydantic import BaseModel


class ModelType(str, Enum):
    INPAINT = "inpaint"  # LaMa, MAT...
    DIFFUSERS_SD = "diffusers_sd"
    DIFFUSERS_SD_INPAINT = "diffusers_sd_inpaint"
    DIFFUSERS_SDXL = "diffusers_sdxl"
    DIFFUSERS_SDXL_INPAINT = "diffusers_sdxl_inpaint"
    DIFFUSERS_OTHER = "diffusers_other"


class HDStrategy(str, Enum):
    # Use original image size
    ORIGINAL = "Original"
    # Resize the longer side of the image to a specific size(hd_strategy_resize_limit),
    # then do inpainting on the resized image. Finally, resize the inpainting result to the original size.
    # The area outside the mask will not lose quality.
    RESIZE = "Resize"
    # Crop masking area(with a margin controlled by hd_strategy_crop_margin) from the original image to do inpainting
    CROP = "Crop"


class LDMSampler(str, Enum):
    ddim = "ddim"
    plms = "plms"


class SDSampler(str, Enum):
    ddim = "ddim"
    pndm = "pndm"
    k_lms = "k_lms"
    k_euler = "k_euler"
    k_euler_a = "k_euler_a"
    dpm_plus_plus = "dpm++"
    uni_pc = "uni_pc"

    lcm = "lcm"


class FREEUConfig(BaseModel):
    s1: float = 0.9
    s2: float = 0.2
    b1: float = 1.2
    b2: float = 1.4


class PowerPaintTask(str, Enum):
    text_guided = "text-guided"
    shape_guided = "shape-guided"
    object_remove = "object-remove"
    outpainting = "outpainting"


class Config(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # Configs for ldm model
    ldm_steps: int = 20
    ldm_sampler: str = LDMSampler.plms

    # Configs for zits model
    zits_wireframe: bool = True

    # Configs for High Resolution Strategy(different way to preprocess image)
    hd_strategy: str = HDStrategy.CROP  # See HDStrategy Enum
    hd_strategy_crop_margin: int = 128
    # If the longer side of the image is larger than this value, use crop strategy
    hd_strategy_crop_trigger_size: int = 800
    hd_strategy_resize_limit: int = 1280

    # Configs for Stable Diffusion 1.5
    prompt: str = ""
    negative_prompt: str = ""
    # Crop image to this size before doing sd inpainting
    # The value is always on the original image scale
    use_croper: bool = False
    croper_x: int = None
    croper_y: int = None
    croper_height: int = None
    croper_width: int = None
    use_extender: bool = False
    extender_x: int = None
    extender_y: int = None
    extender_height: int = None
    extender_width: int = None

    # Resize the image before doing sd inpainting, the area outside the mask will not lose quality.
    # Used by sd models and paint_by_example model
    sd_scale: float = 1.0
    # Blur the edge of mask area. The higher the number the smoother blend with the original image
    sd_mask_blur: int = 0
    # Indicates extent to transform the reference `image`. Must be between 0 and 1. `image` is used as a
    # starting point and more noise is added the higher the `strength`. The number of denoising steps depends
    # on the amount of noise initially added. When `strength` is 1, added noise is maximum and the denoising
    # process runs for the full number of iterations specified in `num_inference_steps`. A value of 1
    # essentially ignores `image`.
    sd_strength: float = 1.0
    # The number of denoising steps. More denoising steps usually lead to a
    # higher quality image at the expense of slower inference.
    sd_steps: int = 50
    # Higher guidance scale encourages to generate images that are closely linked
    # to the text prompt, usually at the expense of lower image quality.
    sd_guidance_scale: float = 7.5
    sd_sampler: str = SDSampler.uni_pc
    # -1 mean random seed
    sd_seed: int = 42
    sd_match_histograms: bool = False

    # out-painting
    sd_outpainting_softness: float = 20.0
    sd_outpainting_space: float = 20.0

    # freeu
    sd_freeu: bool = False
    sd_freeu_config: FREEUConfig = FREEUConfig()

    # lcm-lora
    sd_lcm_lora: bool = False

    # preserving the unmasked area at the expense of some more unnatural transitions between the masked and unmasked areas.
    sd_prevent_unmasked_area: bool = True

    # Configs for opencv inpainting
    # opencv document https://docs.opencv.org/4.6.0/d7/d8b/group__photo__inpaint.html#gga8002a65f5a3328fbf15df81b842d3c3ca05e763003a805e6c11c673a9f4ba7d07
    cv2_flag: str = "INPAINT_NS"
    cv2_radius: int = 4

    # Paint by Example
    paint_by_example_example_image: Optional[Image] = None

    # InstructPix2Pix
    p2p_image_guidance_scale: float = 1.5

    # ControlNet
    enable_controlnet: bool = False
    controlnet_conditioning_scale: float = 0.4
    controlnet_method: str = "lllyasviel/control_v11p_sd15_canny"

    # PowerPaint
    powerpaint_task: PowerPaintTask = PowerPaintTask.text_guided
    # control the fitting degree of the generated objects to the mask shape.
    fitting_degree: float = 1.0
