from typing import Protocol


class FeederJob(Protocol):
    ...


class StackerJob(Protocol):
    ...


class StaplerJob(Protocol):
    ...


class InverterJob(Protocol):
    ...


class PrintJob(FeederJob, StackerJob, StaplerJob, InverterJob):
    ...


class Feeder:
    def __init__(self, job: FeederJob) -> None:
        self.__job = job


class Stacker:
    def __init__(self, job: StackerJob) -> None:
        self.__job = job


class Stapler:
    def __init__(self, job: StaplerJob) -> None:
        self.__job = job


class Inverter:
    def __init__(self, job: InverterJob) -> None:
        self.__job = job


if __name__ == "__main__":
    job = PrintJob()
    feeder = Feeder(job)
    stacker = Stacker(job)
    stapler = Stapler(job)
    inverter = Inverter(job)
