import ffmpeg

f1_2020 = ffmpeg.input('f1_2020.mp4')
outside_overtakes = ffmpeg.input('outside_overtakes.mp4')
#ffmpeg.input('f1_2020.mp4').filter('hflip').output('out.mp4').run()

ffmpeg.filter((f1_2020, outside_overtakes), 'hstack', inputs = 2).output('new_out.mp4', vsync = 2).run()