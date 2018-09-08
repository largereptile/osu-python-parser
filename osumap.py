class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

modes = {0: 'osu!Standard', 1: 'Taiko', 2: 'Catch The Beat', 3: 'osu!Mania', -1: 'no mode'}
# TODO add some kind of enums, do these for type etc. too


class Map():

    def __init__(self, path):
        with open(path, "r", encoding='utf8') as f:
            self.content = f.readlines()
            
        self.key = 'none'
        
        self.categories = {"general": [], "editor": [],
                      "metadata": [], "difficulty": [],
                      "events": [], "timingpoints": [],
                      "colours": [], "hitobjects": [],
                      "none": []}
        
        for line in self.content:
            key = ''.join(e for e in line if e.isalnum()).lower().rstrip()
            if key in self.categories.keys():
                self.key = key
            else:
                self.categories[self.key].append(line.rstrip())

        self.initialise()

    def initialise(self):
        self.parse_general()
        self.parse_editor()
        self.parse_metadata()
        self.parse_difficulty()
        self.parse_events()
        self.parse_hitobjects()
        self.parse_timing_points()
        self.parse_colours()
        self.parse_none()
        
    def parse_none(self):
        self.file_version = self.categories.get('none', ['no version'])[0]

    def parse_general(self):
        temp = {}
        for x in self.categories['general']:
            data = x.split(":", 1)
            if data[0]:
                temp[data[0]] = data[1].lstrip()
        self.general = DotDict()
        self.general.audio_filename = temp.get('AudioFilename', 'no audio')
        self.general.audio_lead_in = int(temp.get('AudioLeadIn', 0))
        self.general.preview_time = int(temp.get('PreviewTime', 0))
        self.general.countdown = int(temp.get('Countdown', 0))
        self.general.sample_set = temp.get('SampleSet', 'none')
        self.general.stack_leniency = float(temp.get('StackLeniency', 0))
        self.general.mode = modes[int(temp.get('Mode', -1))]
        self.general.letterbox_in_breaks = int(temp.get('LetterboxInBreaks', 0))
        self.general.widescreen_storyboard = int(temp.get('WidescreenStoryboard', 0))
        self.general.story_fire_in_front = int(temp.get('StoryFireInFront', 0))
        self.general.special_style = int(temp.get('SpecialStyle', 0))
        self.general.epilepsy_warning = int(temp.get('EpilepsyWarning', 0))
        self.general.use_skin_sprites = int(temp.get('UseSkinSprites', 0))

    def parse_editor(self):
        temp = {}
        for x in self.categories['editor']:
            data = x.split(":", 1)
            if data[0]:
                temp[data[0]] = data[1].lstrip()
        self.editor = DotDict()
        self.editor.bookmarks = temp.get('Bookmarks', "").split(",")
        self.editor.distance_spacing = float(temp.get('DistanceSpacing', 0.0))
        self.editor.beat_divisior = int(temp.get('BeatDivisor', 0))
        self.editor.grid_size = int(temp.get('GridSize', 0))
        self.editor.timeline_zoom = float(temp.get('TimelineZoom', 1))

    def parse_metadata(self):
        temp = {}
        for x in self.categories['metadata']:
            data = x.split(":", 1)
            if data[0]:
                temp[data[0]] = data[1].lstrip()
        self.title = temp.get('TitleUnicode', temp['Title'])
        self.artist = temp.get('ArtistUnicode', temp['Artist'])
        self.creator = temp.get('Creator', 'no mapper')
        self.version = temp.get('Version', 'no difficulty')
        self.source = temp.get('Source', 'no source')
        self.tags = temp.get('Tags', 'none')
        self.id = int(temp.get('BeatmapID', 0))
        self.set_id = int(temp.get('BeatmapSetID', 0))

    def parse_difficulty(self):
        temp = {}
        for x in self.categories['difficulty']:
            data = x.split(":", 1)
            if data[0]:
                temp[data[0]] = data[1].lstrip()
        self.difficulty = DotDict()
        self.difficulty.hp_drain_rate = int(temp.get('HPDrainRate', 0))
        self.difficulty.circle_size = float(temp.get('CircleSize', 0.0))
        self.difficulty.overall_difficulty = float(temp.get('OverallDifficulty', 0.0))
        self.difficulty.approach_rate = float(temp.get('ApproachRate', 0.0))
        self.difficulty.slider_multiplier = float(temp.get('SliderMultiplier', 0.0))
        self.difficulty.slider_tick_rate = float(temp.get('SliderTickRate', 0.0))

    def parse_events(self):
        self.events = []
        for x in self.categories['events']:
            if not x.startswith("//"):
                self.events.append(x)

    def parse_timing_points(self):
        self.timing_points = DotDict()
        for x in self.categories['timingpoints']:
            cats = x.split(",")
            if not cats[0]:
                break
            offset = cats[0]
            self.timing_points[offset] = DotDict()
            self.timing_points[offset].mpb = float(cats[1])
            self.timing_points[offset].meter = int(cats[2])
            self.timing_points[offset].sample_set = int(cats[3])
            self.timing_points[offset].sample_index = int(cats[4])
            self.timing_points[offset].volume = int(cats[5])
            self.timing_points[offset].inherited = int(cats[6])
            self.timing_points[offset].kiai = int(cats[7])

    def parse_colours(self):
        self.colours = DotDict()
        for x in self.categories['colours']:
            data = x.split(":", 1)
            if data[0]:
                self.colours[data[0]] = data[1]

    def parse_hitobjects(self):
        self.hitobjects = DotDict()
        for x in self.categories['hitobjects']:
            cats = x.split(",", 5)
            offset = int(cats[2])
            self.hitobjects[offset] = DotDict()
            self.hitobjects[offset].x = int(cats[0])
            self.hitobjects[offset].y = int(cats[1])
            self.hitobjects[offset].type = int(cats[3])
            self.hitobjects[offset].hitsound = int(cats[4])
            if int(cats[3]) == 2 or int(cats[3]) == 6:
                cats2 = cats[5].split(",")
                path = cats2[0].split("|")
                self.hitobjects[offset].slider_type = path[0]
                self.hitobjects[offset].curve_points = DotDict()
                count = 0
                for point in path[1:]:
                    points = point.split(":")
                    self.hitobjects[offset].curve_points[count] = points
                    count += 1
                self.hitobjects[offset].repeat = int(cats2[1])
                self.hitobjects[offset].pixel_length = float(cats2[2])
                self.hitobjects[offset].edge_hitsounds = cats2[3].split("|")
                self.hitobjects[offset].edge_additions = cats2[4].split("|")
                self.hitobjects[offset].extras = cats2[5]
            elif int(cats[3]) == 8 or int(cats[3]) == 12:
                cats2 = cats[5].split(",")
                self.hitobjects[offset].end_time = cats2[0]
                self.hitobjects[offset].extras = cats2[1]
            else:
                self.hitobjects[offset].extras = cats[5]
