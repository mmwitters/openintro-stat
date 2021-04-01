from random import random
from math import sqrt


class BernoulliTrial:
    def __init__(self, probability):
        self.probability = probability

    def __str__(self):
        return "BernoulliTrial({probability})".format(probability=self.probability)

    def mean(self):
        return self.probability

    def std_dev(self):
        return sqrt(self.probability * (1 - self.probability))

    def random_run(self):
        random_number = random()
        if random_number < self.probability:
            return True
        else:
            return False

    def and_also(self, other):
        return BernoulliTrial(self.probability * other.probability)


class BinomialDistribution:
    def __init__(self, num_trials: int, bernoulli_trial):
        self.bernoulli_trial = bernoulli_trial
        self.num_trials = num_trials

    def __str__(self):
        return "BinomialDistribution({num_trials}, {bernoulli_trial})".format(num_trials=self.num_trials,
                                                                              bernoulli_trial=self.bernoulli_trial)

    def mean(self):
        return self.bernoulli_trial.mean() * self.num_trials

    def std_dev(self):
        probability = self.bernoulli_trial.probability
        return sqrt(self.num_trials * probability * (1 - probability))

    def random_run(self):
        count = 0
        for i in range(self.num_trials):
            success = self.bernoulli_trial.random_run()
            if success:
                count += 1
        return count


class GeometricDistribution:
    def __init__(self, bernoulli_trial):
        self.bernoulli_trial = bernoulli_trial

    def __str__(self):
        return "GeometricDistribution({trial})".format(trial=self.bernoulli_trial)

    def mean(self):
        return 1.0 / self.bernoulli_trial.probability

    def std_dev(self):
        return sqrt((1 - self.bernoulli_trial.probability) / (self.bernoulli_trial.probability ** 2))

    def random_run(self):
        reach_success = False
        num_trials = 0
        while not reach_success:
            num_trials += 1
            result = self.bernoulli_trial.random_run()
            if result:
                reach_success = True
        return num_trials - 1


def sample_deviation(distribution):
    sample = distribution.random_run()
    deviation = sample - distribution.mean()
    return abs(deviation)


def multi_sample_deviation(distribution, n):
    deviation_list = []
    for i in range(n):
        deviation_list.append(sample_deviation(distribution))
    return deviation_list


def sample_variance_sqrt(deviations):
    total = 0
    for item in deviations:
        total += item ** 2
    return sqrt(total / (len(deviations) - 1))


def sample_zscore(distribution):
    dev = sample_deviation(distribution)
    z = dev / distribution.std_dev()
    return z


def sample_mean(distribution, n):
    total = 0.0
    for i in range(n):
        run = distribution.random_run()
        total += run
    return total / n


def print_distribution_summary(distribution, sample_size=1000):
    print(str(distribution))
    print("\tMean: ", distribution.mean())
    print("\tSqrt of Sample Variance: ", sample_variance_sqrt(multi_sample_deviation(distribution, sample_size)))
    print("\tStandard Deviation: ", distribution.std_dev())
    print("\tZ-Score: ", sample_zscore(distribution))
    print("\tSample: ", distribution.random_run())
    print("\tSample Mean: ", sample_mean(distribution, sample_size))


roll_six = BernoulliTrial(1.0 / 6)
heads = BernoulliTrial(0.5)
roll_six_and_heads = roll_six.and_also(heads)
both_dist = BinomialDistribution(12, roll_six_and_heads)

print_distribution_summary(heads, 10000)
print()
print_distribution_summary(roll_six, 1000)
print()
print_distribution_summary(both_dist, 100)
