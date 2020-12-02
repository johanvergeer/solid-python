class ValidatableStr(str):
    def __init__(self, value, attribute_name, max_length=10):
        self.__attribute_name = attribute_name
        self.__max_length = max_length
        str.__init__(self)

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, args[0])

    def validate(self):
        if len(self) > self.__max_length:
            raise ValueError(
                f'Value of "{self.__attribute_name}" is longer than {self.__max_length}. ({self})'
            )


class ValidatableDescriptor:
    def __init__(self, max_length: int) -> None:
        self.__max_length = max_length

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __set__(self, instance, value):
        setattr(
            instance,
            self.private_name,
            # ValidatableStr(value, self.public_name),
            ValidatableStr(value, self.public_name, max_length=self.__max_length),
        )

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, "")


class DescriptorUser:
    field = ValidatableDescriptor(10)


d = DescriptorUser()
d.field = "something pretty long"

# print(d.field)
#
# d2 = DescriptorUser()
# d2.field = "20"
#
# print(d2.field)
# print(d.field)
#
d.field.validate()
