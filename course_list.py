from course import Course


class CourseList:
    elements = []
    periods = 0

    def __init__(self, num_of_courses, num_of_slots):
        self.periods = num_of_slots
        self.elements = [Course(i) for i in range(num_of_courses)]

    #how the data is stored in the datatset?
    def read_clashes(self, filename):
        with open(f'course_files/{filename}', 'r') as f:
            instrument_list = f.read().splitlines()
            # elements = [Course(i) for i in range(0, len(instrument_list))]
            for line in instrument_list:
                courses = line.split(" ")
                for i in range(0, len(courses)):
                    for j in range(0, len(courses)):
                        if (courses[i] and courses[j]) and i != j:
                            self.elements[int(courses[i])].add_clash(self.elements[int(courses[j])])

    def length(self):
        return len(self.elements)

    def status(self, index):
        return self.elements[index].clash_size()

    def slot(self, index):
        return self.elements[index].my_slot

    def set_slot(self, index, slot):
        self.elements[index].my_slot = slot

    def clashes_left(self):
        result = 0
        for i in self.elements:
            result += i.clash_size()
        return result

    def iterate_element(self, element, iterations):
        element.set_is_clash()
        iterate = 1
        current_slot = element.my_slot
        while iterate <= iterations and element.is_clash != 0:
            element.set_is_clash()
            element.shift(self.periods)
            iterate += 1
            # print(f"{element.course_id} {element.my_slot}")
        return (self.periods*iterate)+current_slot

    def iterate(self, iterations):
        actions = []
        for i in self.elements:
            actions.append(self.iterate_element(i, iterations))
        return actions


    def iterate_based_iterations(self, iterations):
        actions = []
        for i in range(len(self.elements)):
            self.iterate_element(self.elements[i], iterations[i])
        return actions

    def iterate_based_on_actions(self, actions):
        for i in range(len(self.elements)):
            self.elements[i].set_is_clash()
            self.elements[i].shift_slot(self.periods, int(actions[i]))
            # print(f"{self.elements[i].course_id} {self.elements[i].my_slot}")

    def print_result(self):
        for i in self.elements:
            print(f"{i}    {i.my_slot}")

