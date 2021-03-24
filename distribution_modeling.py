from random import random
from math import sqrt


class BernoulliTrial:
    def __init__(self, probability):
        self.probability = probability

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
    def __init__(self, num_trials, bernoulli_trial):
        self.bernoulli_trial = bernoulli_trial
        self.num_trials = num_trials

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


roll_six = BernoulliTrial(0.16)
both_outcomes = roll_six.and_also(BernoulliTrial(0.5))
both_dist = BinomialDistribution(100, roll_six)
print("This is the mean", both_dist.mean())
print("This is sqrt of sample variance", sample_variance_sqrt(multi_sample_deviation(both_dist, 10000)))
print("This is standard deviation", both_dist.std_dev())
print("This is z score", sample_zscore(both_dist))
