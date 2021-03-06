import unittest
import alang
import tqdm


class TestSampleTuringMachines(unittest.TestCase):
    def test_copy(self):
        copy_machine = alang.TuringMachine.from_file("example_machines/copy.yaml")
        copy_machine.init_tape("input", ["0", "1", "0", "0", "1"])
        for i in range(10):
            try:
                copy_machine.step()
            except alang.TMHalt as e:
                for key in copy_machine.tapes["input"].tape:
                    self.assertEqual(copy_machine.tapes["input"].tape[key], copy_machine.tapes["output"].tape[key])
                    self.assertEqual(len(copy_machine.tapes["input"].tape), len(copy_machine.tapes["output"].tape))
                self.assertEqual(e.halting_instruction, "halt")
                return
        self.assertEqual(True, False)

    def test_palindrome(self):
        palindrome_machine = alang.TuringMachine.from_file("example_machines/palindrome.yaml")

        nb_success = 0

        tests = [(["0", "1", "0", "0", "1"], False), ((["1", "0", "0", "1"], True))]

        for test in tests:
            palindrome_machine.reset()
            palindrome_machine.init_tape("input", test[0])
            for i in range(30):
                try:
                    palindrome_machine.step()

                except alang.TMHalt as e:
                    self.assertEqual(e.halting_instruction, "palindrome" if test[1] else "not_palindrome")
                    nb_success += 1
                    break

        self.assertEqual(nb_success, len(tests))

    def test_parity(self):
        parity_machine = alang.TuringMachine.from_file("example_machines/parity.yaml")

        tests = [(["0", "1", "0", "0", "1"], "0"), (["1", "0", "0", "1", "1"], "1"), (["1", "0", "1", "1", "1"], "0")]

        for test in tests:
            parity_machine.reset()
            parity_machine.init_tape("input", test[0])
            for i in range(30):
                try:
                    parity_machine.step()

                except alang.TMHalt as e:
                    self.assertEqual(e.halting_instruction, "halt")
                    self.assertEqual(parity_machine.tapes["output"].tape[0], test[1])
                    break

    def test_parity_adder(self):
        adder_machine = alang.TuringMachine.from_file("example_machines/binary_adder.yaml")

        tests = [(["1"], ["1"], ["0", "1"]), (["1"], ["0"], ["1"]), (["0", "1"], ["0", "1"], ["0", "0", "1"])]

        for test in tests:
            adder_machine.reset()
            adder_machine.init_tape("input_1", test[0])
            adder_machine.init_tape("input_2", test[1])
            for i in range(30):
                try:
                    adder_machine.step()

                except alang.TMHalt as e:
                    self.assertEqual(e.halting_instruction, "halt")
                    for i, s in enumerate(test[2]):
                        self.assertEqual(adder_machine.tapes["output"].tape[i], s)
                    break


class TestBusyBeavers(unittest.TestCase):
    # cf: http://www.logique.jussieu.fr/~michel/ha.html#tm52
    # cf: https://www.scottaaronson.com/papers/bb.pdf
    def test_busy_beaver_5_2(self):
        # Current contender for 5 states 2 symbols
        busy_beaver = alang.TuringMachine.from_file("example_machines/busy_beaver_contender_5_2.yaml")
        should_stop_after = 47176870

        has_stopped = False
        for i in tqdm.tqdm(range(should_stop_after)):
            try:
                busy_beaver.step()
            except alang.TMHalt:
                has_stopped = True
                break

        self.assertTrue(has_stopped)
        self.assertEqual(i + 1, should_stop_after)  # i+1 because tick needed to take the Halting transition
