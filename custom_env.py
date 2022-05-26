from gym import Env
from gym.spaces import MultiDiscrete, Discrete
from course_list import CourseList
import numpy


class CourseEnv(Env):
    def __init__(self, num_courses, slots, clash_file, steps):

        self.slots = slots
        self.clash_file = clash_file
        self.num_courses = num_courses
        self.courses = CourseList(num_courses, slots)
        self.courses.read_clashes(clash_file)
        self.min_slots = [0] * num_courses
        self.min_val = 1000000000
        self.current_step = 0
        self.average = 0
        for i in range(len(self.min_slots)):
            self.courses.set_slot(i, self.min_slots[i])
        self.max_clash = self.courses.clashes_left()

        self.action_space = Discrete(2*slots)
        self.observation_space = MultiDiscrete([slots+1]*num_courses)
        self.set_state()
        self.steps = steps

    def set_state(self):
        self.state = numpy.array([i.my_slot for i in self.courses.elements])

    def step(self, action):
        self.current_step += 1
        self.courses.iterate(action)
        clashes = self.courses.clashes_left()
        self.set_state()


        if clashes <= self.max_clash:

            reward = self.max_clash - clashes
            self.max_clash = clashes
        else:
            reward = self.max_clash - clashes

        if self.current_step == self.steps or clashes == 0:
            done = True
        else:
            done = False

        info = {"clashes": clashes}

        return self.state, reward, done, info

    def render(self):
        pass

    def reset(self):
        self.courses = CourseList(self.num_courses, self.slots)
        self.courses.read_clashes(self.clash_file)
        self.min_slots = [0] * self.num_courses
        self.min_val = 1000000000
        self.current_step = 0
        self.average = 0
        for i in range(len(self.min_slots)):
            self.courses.set_slot(i, self.min_slots[i])

        self.set_state()
        return self.state