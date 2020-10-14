

class Marking:

    def __init__(self, mode):
        self.total_mark = 0
        if mode == 'driving':
            self.is_object_met = False
            self.is_over_time = False
            self.collision_times = 0
            self.too_close_times = 0
        elif mode == 'detect':
            self.detect_num = 0
            self.total_target = 0
            self.correct_target = 0
            self.detect_time = 0
            self.detect_str = ''
            self.answer_str = ''

    def detect_marking(self, detecteds, targets, cost_time):
        target_length = len(targets)
        detect_length = len(detecteds)
        loop_times = target_length if target_length <= detect_length else detect_length

        for detect in detecteds:
            self.detect_str += detect + ';'

        self.detect_str += '|'

        for target in targets:
            self.answer_str += target + ';'

        self.answer_str += '|'

        for i in range(loop_times):
            if targets[i] == detecteds[i]:
                self.correct_target += 1

        self.total_target += target_length
        self.detect_num += 1
        self.detect_time += cost_time

    def detect_result(self):
        accuracy = self.correct_target / self.total_target
        average_cost_time = self.detect_time / self.detect_num
        time_mark = 0
        if average_cost_time < 0.2:
            time_mark = 30
        elif average_cost_time < 0.5:
            time_mark = 20
        elif average_cost_time < 1:
            time_mark = 10

        final_mark = (70 + time_mark) * accuracy
        average_cost_time = round(average_cost_time, 2)
        final_mark = round(final_mark, 2)
        accuracy = round(accuracy * 100, 2)
        print('Accuracy: ', accuracy, "%, Average Time: ", average_cost_time, "s, Mark: ", final_mark)
        return accuracy, average_cost_time, final_mark, self.detect_str, self.answer_str




