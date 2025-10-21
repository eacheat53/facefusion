import os
import json
import secrets
from datetime import datetime, timezone

# 这是一个从您提供的JSON文件中提取出来的参数模板。
# 它包含了所有处理效果的设置，我们只需要在每次循环时更改路径即可。
ARGS_TEMPLATE = {
    "face_detector_model": "yunet",
    "face_detector_angles": [0],
    "face_detector_size": "640x640",
    "face_detector_score": 0.5,
    "face_landmarker_model": "2dfan4",
    "face_landmarker_score": 0.5,
    "face_selector_mode": "reference",
    "face_selector_order": "large-small",
    "face_selector_gender": "female",
    "face_selector_race": "asian",
    "face_selector_age_start": None,
    "face_selector_age_end": None,
    "reference_face_position": 0,
    "reference_face_distance": 0.3,
    "reference_frame_number": 0,
    "face_occluder_model": "xseg_3",
    "face_parser_model": "bisenet_resnet_34",
    "face_mask_types": ["occlusion"],
    "face_mask_areas": ["upper-face", "lower-face", "mouth"],
    "face_mask_regions": [
        "skin", "left-eyebrow", "right-eyebrow", "left-eye", "right-eye",
        "glasses", "nose", "mouth", "upper-lip", "lower-lip"
    ],
    "face_mask_blur": 0.3,
    "face_mask_padding": [0, 0, 0, 0],
    "voice_extractor_model": "kim_vocal_2",
    "trim_frame_start": None,
    "trim_frame_end": None,
    "temp_frame_format": "png",
    "keep_temp": None,
    "output_image_quality": 80,
    "output_image_scale": 1.0,
    "output_audio_encoder": "flac",
    "output_audio_quality": 80,
    "output_audio_volume": 100,
    "output_video_encoder": "h264_nvenc",
    "output_video_preset": "veryfast",
    "output_video_quality": 80,
    "output_video_scale": 1.0,
    "output_video_fps": None,
    "processors": ["face_swapper", "face_enhancer", "expression_restorer"],
    "age_modifier_model": "styleganex_age",
    "age_modifier_direction": 0,
    "deep_swapper_model": "iperov/elon_musk_224",
    "deep_swapper_morph": 100,
    "expression_restorer_model": "live_portrait",
    "expression_restorer_factor": 100,
    "expression_restorer_areas": ["upper-face", "lower-face"],
    "face_debugger_items": ["face-landmark-5/68", "face-mask"],
    "face_editor_model": "live_portrait",
    "face_editor_eyebrow_direction": 0.0,
    "face_editor_eye_gaze_horizontal": 0.0,
    "face_editor_eye_gaze_vertical": 0.0,
    "face_editor_eye_open_ratio": 0.0,
    "face_editor_lip_open_ratio": 0.0,
    "face_editor_mouth_grim": 0.0,
    "face_editor_mouth_pout": 0.0,
    "face_editor_mouth_purse": 0.0,
    "face_editor_mouth_smile": 0.0,
    "face_editor_mouth_position_horizontal": 0.0,
    "face_editor_mouth_position_vertical": 0.0,
    "face_editor_head_pitch": 0.0,
    "face_editor_head_yaw": 0.0,
    "face_editor_head_roll": 0.0,
    "face_enhancer_model": "gpen_bfr_512",
    "face_enhancer_blend": 80,
    "face_enhancer_weight": 0.5,
    "face_swapper_model": "hyperswap_1a_256",
    "face_swapper_pixel_boost": "512x512",
    "face_swapper_weight": 0.7,
    "frame_colorizer_model": "ddcolor",
    "frame_colorizer_blend": 100,
    "frame_colorizer_size": "256x256",
    "frame_enhancer_model": "span_kendata_x4",
    "frame_enhancer_blend": 80,
    "lip_syncer_model": "wav2lip_gan_96",
    "lip_syncer_weight": 0.5
}

def create_job_file(source_path, destination_path, output_json_path="job.json"):
    """
    根据源图片和目标路径生成一个FaceFusion的job.json文件。
    destination_path可以是单张图片或文件夹路径。
    """
    if not os.path.isfile(source_path):
        print(f"错误：源文件不存在 -> {source_path}")
        return

    steps = []
    target_files = []
    
    # 检查目标路径是文件还是文件夹
    if os.path.isfile(destination_path):
        # 单张图片或视频
        if destination_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.mp4')):
            target_files.append(destination_path)
        else:
            print(f"错误：目标文件不是支持的格式 -> {destination_path}")
            return
    elif os.path.isdir(destination_path):
        # 文件夹 - 遍历所有支持的图片和视频文件
        for filename in os.listdir(destination_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.mp4')):
                target_files.append(os.path.join(destination_path, filename))
    else:
        print(f"错误：目标路径不存在 -> {destination_path}")
        return

    if not target_files:
        print(f"警告：在路径 '{destination_path}' 中没有找到任何支持的文件格式。")
        return

    # 获取任务名称（从输出文件名中提取，去掉.json后缀）
    job_name = os.path.splitext(os.path.basename(output_json_path))[0]
    
    # 为每个目标文件创建任务步骤
    for index, target_path in enumerate(target_files, 1):
        # 创建一个模板的副本进行修改
        args = ARGS_TEMPLATE.copy()

        # 根据目标文件类型调整参数
        if target_path.lower().endswith('.mp4'):
            # MP4视频处理的特殊配置
            args['processors'] = ["face_swapper", "expression_restorer"]
            args['face_enhancer_model'] = "gfpgan_1.4"
            args['face_selector_gender'] = "female"
            args['face_selector_race'] = "asian"

        # 设置动态路径
        args['source_paths'] = [os.path.abspath(source_path)]
        args['target_path'] = os.path.abspath(target_path)
        
        # 使用任务名称加上顺序号作为输出文件名（带连字符分隔）
        # 根据目标文件扩展名决定输出扩展名，保持一致
        target_extension = os.path.splitext(target_path)[1].lower()
        if target_extension:
            output_filename = f"{job_name}-{index}{target_extension}"
        else:
            # 如果没有扩展名，默认使用.jpg
            output_filename = f"{job_name}-{index}.jpg"
        args['output_path'] = os.path.abspath(os.path.join("output", output_filename))

        # 构建一个任务步骤
        step = {
            "args": args,
            "status": "queued"
        }
        steps.append(step)

    # 获取当前时间戳
    now = datetime.now(timezone.utc).astimezone().isoformat()

    # 构建最终的job文件结构
    final_job = {
        "version": "1",
        "date_created": now,
        "date_updated": now,
        "steps": steps
    }

    # 写入JSON文件
    try:
        # 确保.jobs/queued文件夹存在
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        # 同时确保output文件夹存在（用于处理结果）
        os.makedirs("output", exist_ok=True)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(final_job, f, indent=4, ensure_ascii=False)
        print(f"成功！已生成 {len(steps)} 个任务。")
        print(f"任务文件已保存至: {os.path.abspath(output_json_path)}")
        print("现在您可以使用 'job-run' 命令来执行这个任务文件。")
    except Exception as e:
        print(f"错误：无法写入JSON文件 -> {e}")


if __name__ == '__main__':
    # 在终端中提示用户输入路径
    print("=== FaceFusion 批量处理任务生成器 ===")
    print("提示：可以直接将图片或文件夹拖拽到终端窗口")
    print()
    
    # 获取源图片路径
    while True:
        source_path = input("请输入源脸部图片的文件路径 (src) [可拖拽]: ").strip()
        # 移除可能的引号
        source_path = source_path.strip('"').strip("'")
        
        if not source_path:
            print("错误：路径不能为空，请重新输入。")
            continue
            
        # 检查文件是否存在
        if os.path.isfile(source_path):
            # 检查是否为图片文件
            if source_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')):
                break
            else:
                print("错误：请输入一个有效的图片文件（支持：jpg, jpeg, png, bmp, tiff, webp）。")
        else:
            print(f"错误：文件不存在 -> {source_path}")
            print("请检查路径是否正确，或尝试使用绝对路径。")
    
    # 获取目标路径（可以是单张图片或文件夹）
    while True:
        destination_path = input("请输入目标路径 (dst) [支持单张图片或文件夹，可拖拽]: ").strip()
        # 移除可能的引号
        destination_path = destination_path.strip('"').strip("'")
        
        if not destination_path:
            print("错误：路径不能为空，请重新输入。")
            continue
            
        if os.path.isfile(destination_path):
            # 单张图片或视频
            if destination_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')):
                print(f"检测到单张图片: {os.path.basename(destination_path)}")
                break
            elif destination_path.lower().endswith('.mp4'):
                print(f"检测到MP4视频: {os.path.basename(destination_path)}")
                break
            else:
                print("错误：单张文件只支持图片格式（JPG/JPEG/PNG/BMP/TIFF/WEBP）或MP4格式。")
        elif os.path.isdir(destination_path):
            # 文件夹 - 检查是否有支持的文件
            supported_files = [f for f in os.listdir(destination_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.mp4'))]
            if supported_files:
                image_count = len([f for f in supported_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'))])
                mp4_count = len([f for f in supported_files if f.lower().endswith('.mp4')])
                print(f"检测到文件夹，找到 {image_count} 个图片文件和 {mp4_count} 个MP4文件。")
                break
            else:
                print(f"警告：文件夹中没有找到支持的文件格式，是否继续？ (y/n): ")
                choice = input().strip().lower()
                if choice in ['y', 'yes', '是']:
                    break
        else:
            print(f"错误：路径不存在 -> {destination_path}")
            print("请检查路径是否正确，或尝试使用绝对路径。")
    
    # 获取输出文件名（可选）
    output_filename = input("请输入输出的JSON文件名 (默认为自动生成): ").strip()
    if not output_filename:
        # 自动生成基于日期时间的文件名
        # 使用绝对路径指向项目根目录下的.jobs/queued
        script_dir = os.path.dirname(os.path.abspath(__file__))
        queued_dir = os.path.join(script_dir, ".jobs", "queued")
        
        # 获取当前日期时间格式为 YY-MM-DD-HH-MM
        current_datetime = datetime.now().strftime("%y-%m-%d-%H-%M")
        
        try:
            os.makedirs(queued_dir, exist_ok=True)
            # 直接使用时间作为文件名，不需要序号
            output_filename = f"{current_datetime}.json"
        except:
            output_filename = f"{current_datetime}.json"
    
    # 确保输出文件保存在.jobs/queued目录下
    if not output_filename.endswith('.json'):
        output_filename += '.json'
    
    # 使用绝对路径构建输出文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, ".jobs", "queued", output_filename)
    
    print()
    print(f"源图片: {source_path}")
    print(f"目标路径: {destination_path}")
    print(f"输出文件: {output_path}")
    print()
    
    # 运行主函数
    create_job_file(source_path, destination_path, output_path)