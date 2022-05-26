from stable_baselines3 import PPO
from custom_env import CourseEnv

problems = {
    "hec-s-92.stu": {"courses": 82,
                     "slot": 19,
                     "timestamp": 100000,
                     "steps": 15000},
    "sta-f-83.stu": {"courses": 140,
                     "slot": 13,
                     "timestamp": 5000,
                     "steps": 1500},
    "lse-f-91.stu": {"courses": 382,
                     "slot": 21,
                     "timestamp": 8000,
                     "steps": 15000},
    "yor-f-83.stu": {"courses": 182,
                     "slot": 24,
                     "timestamp": 5000,
                     "steps": 20000},
    "ear-f-83.stu": {"courses": 191,
                     "slot": 26,
                     "timestamp": 100000,
                     "steps": 20000},
    "kfu-s-93.stu": {"courses": 462,
                     "slot": 21,
                     "timestamp": 30000,
                     "steps": 100000},
    "tre-s-92.stu": {"courses": 262,
                     "slot": 25,
                     "timestamp": 100000,
                     "steps": 30000},
    "rye-s-93.stu": {"courses": 488,
                     "slot": 25,
                     "timestamp": 30000,
                     "steps": 30000},
    "ute-s-92.stu": {"courses": 185,
                     "slot": 10,
                     "timestamp": 5000,
                     "steps": 1500}
}

if __name__ == "__main__":
    for i in problems:
        env = CourseEnv(num_courses=problems[i]["courses"], slots=problems[i]["slot"], clash_file=i,
                        steps=problems[i]["steps"])
        model = PPO('MlpPolicy', env, verbose=1)
        model.learn(total_timesteps=problems[i]["timestamp"])
        env.close()
        model.save(f"{i}_model")
        del model
        with open("results.txt", "a") as file:
            model = PPO.load(f"{i}_model", env=env)
            obs = env.reset()
            done = False
            min_clashes = 100000000
            max_iterations = None
            while not done:
                action, _states = model.predict(obs)
                obs, rewards, done, info = env.step(action)
                if min_clashes >= info["clashes"]:
                    min_clashes = info["clashes"]
                    max_iterations = action
                print(obs, rewards, done, info)
            file.write(f"problem {i}, max_iterations: {max_iterations}, min_clashes: {min_clashes}\n")
