class Course:
    is_clash = 0

    def __init__(self, course_id, slot=None):
        self.course_id = course_id
        self.clashes_with = set()
        self.my_slot = slot or 0
        self.is_clash = 0

    def add_clash(self, clash):
        self.clashes_with.add(clash)

    def clash_size(self):
        result = 0
        for i in self.clashes_with:
            if self.my_slot == i.my_slot:
                result += 1
        return result

    def return_clashes(self):
        result = []
        for i in self.clashes_with:
            if self.my_slot == i.my_slot:
                result.append(i)
        return result

    def unit_clash_force(self):
        for i in self.clashes_with:
            if self.my_slot == i.my_slot:
                return 1
        return 0

    def set_is_clash(self):
        self.is_clash = self.unit_clash_force()

    def shift(self, limit):
        self.my_slot += self.is_clash
        if self.my_slot < 0:
            self.my_slot = limit - 1
        elif self.my_slot >= limit:
            self.my_slot = 0

    def shift_slot(self, limit, sift_param):
        my_slot = self.my_slot
        my_slot += sift_param
        if my_slot > limit:
            my_slot = my_slot % limit
        self.my_slot = my_slot
