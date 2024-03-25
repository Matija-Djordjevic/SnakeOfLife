import json 

alo_be = dict()

alo_be["colors"] = dict()

alo_be["colors"]["red"]       = (255, 0, 0) 
alo_be["colors"]["black"]     = (0, 0, 0) 
alo_be["colors"]["blue"]      = (0, 0, 255) 
alo_be["colors"]["lime"]      = (0, 255, 0) 
alo_be["colors"]["yellow"]    = (255, 255, 0) 
alo_be["colors"]["white"]     = (255, 255, 255) 
alo_be["colors"]["gray"]      = (128, 128, 128) 
alo_be["colors"]["green"]     = (0, 128, 0) 
alo_be["colors"]["cyan"]      = (0, 255, 255) 
alo_be["colors"]["aqua"]      = (0, 255, 255) 
alo_be["colors"]["zima_blue"] = (22, 184, 243)

alo_be["colors"]["github_green_4"] = (57, 211, 83)
alo_be["colors"]["github_green_3"] = (38, 166, 65)
alo_be["colors"]["github_green_2"] = (0, 109, 50)
alo_be["colors"]["github_green_1"] = (12, 74, 42)
alo_be["colors"]["github_inactive"] = (22, 27, 34)
alo_be["colors"]["github_background"] = (13, 17, 23)

alo_be ['resolutions'] = dict()

alo_be['resolutions']['hd']          = (1280, 720)
alo_be['resolutions']['full_hd']     = (1920, 1080)
alo_be['resolutions']['two_k']       = (2560, 1440)
alo_be['resolutions']['four_k']      = (3840, 2160)
alo_be['resolutions']['eight_k']     = (7680, 4320)
alo_be['resolutions']['large_box']   = (1300, 1300)
alo_be['resolutions']['medium_box']  = (900, 900)
alo_be['resolutions']['small_box']   = (500, 500)
alo_be['resolutions']['github_activity']   = (1920, 265)

alo_be['icon'] = dict()
alo_be['icon']['folder'] = 'assets'
alo_be['icon']['name'] = 'icon.png'

alo_be['window'] = dict()
alo_be['window']['name'] = 'Snake of Life' 

alo_be['frames'] = dict()
alo_be['frames']['game_ticks'] = 144
alo_be['frames']['fps_cap'] = 144
alo_be['frames']['updates_per_cycle'] = 1


if __name__ == '__main__':
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(alo_be, f, ensure_ascii=True, indent=2)
        
    with open('data.json', 'r', encoding='utf-8') as f:
        neki = json.load(f)
        print(neki)