class PrintJob:
    pass


class Feeder:
    def __init__(self, job: PrintJob) -> None:
        self.__job = job


class Stacker:
    def __init__(self, job: PrintJob) -> None:
        self.__job = job


class Stapler:
    def __init__(self, job: PrintJob) -> None:
        self.__job = job


class Inverter:
    def __init__(self, job: PrintJob) -> None:
        self.__job = job


if __name__ == "__main__":
    job = PrintJob()
    feeder = Feeder(job)
    stacker = Stacker(job)
    stapler = Stapler(job)
    inverter = Inverter(job)
