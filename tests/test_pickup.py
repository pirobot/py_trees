#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/py_trees/devel/LICENSE
#
##############################################################################
# Imports
##############################################################################

import py_trees
import py_trees.console as console

##############################################################################
# Logging Level
##############################################################################

py_trees.logging.level = py_trees.logging.Level.DEBUG
logger = py_trees.logging.Logger("Nosetest")

##############################################################################
# Tests
##############################################################################


def test_high_priority_interrupt():
    console.banner("High Priority Interrupt")
    task_one = py_trees.behaviours.Count(
        name="Task 1",
        fail_until=0,
        running_until=2,
        success_until=10
    )
    task_two = py_trees.behaviours.Count(
        name="Task 2",
        fail_until=0,
        running_until=2,
        success_until=10
    )
    high_priority_interrupt = py_trees.meta.running_is_failure(
        py_trees.behaviours.Periodic)(
        name="High Priority",
        n=3
    )
    piwylo = py_trees.idioms.pick_up_where_you_left_off(
        name="Pick Up\nWhere You\nLeft Off",
        tasks=[task_one, task_two]
    )
    root = py_trees.composites.Selector(name="Root")
    root.add_children([high_priority_interrupt, piwylo])

    py_trees.display.print_ascii_tree(root)
    visitor = py_trees.visitors.DebugVisitor()
    py_trees.tests.tick_tree(root, visitor, 1, 3)
    print()

    print("\n--------- Assertions ---------\n")
    print("high_priority_interrupt.status == py_trees.common.Status.FAILURE")
    assert(high_priority_interrupt.status == py_trees.common.Status.FAILURE)
    print("piwylo.status == py_trees.common.Status.RUNNING")
    assert(piwylo.status == py_trees.common.Status.RUNNING)
    print("task_one.status == py_trees.common.Status.SUCCESS")
    assert(task_one.status == py_trees.common.Status.SUCCESS)
    print("task_two.status == py_trees.common.Status.RUNNING")
    assert(task_two.status == py_trees.common.Status.RUNNING)

    py_trees.tests.tick_tree(root, visitor, 4, 5)

    print("\n--------- Assertions ---------\n")
    print("high_priority_interrupt.status == py_trees.common.Status.SUCCESS")
    assert(high_priority_interrupt.status == py_trees.common.Status.SUCCESS)
    print("piwylo.status == py_trees.common.Status.INVALID")
    assert(piwylo.status == py_trees.common.Status.INVALID)
    print("task_one.status == py_trees.common.Status.INVALID")
    assert(task_one.status == py_trees.common.Status.INVALID)
    print("task_two.status == py_trees.common.Status.INVALID")
    assert(task_two.status == py_trees.common.Status.INVALID)

    py_trees.tests.tick_tree(root, visitor, 6, 8)

    print("\n--------- Assertions ---------\n")
    print("high_priority_interrupt.status == py_trees.common.Status.FAILURE")
    assert(high_priority_interrupt.status == py_trees.common.Status.FAILURE)
    print("piwylo.status == py_trees.common.Status.RUNNING")
    assert(piwylo.status == py_trees.common.Status.RUNNING)
    print("task_one.status == py_trees.common.Status.INVALID")
    assert(task_one.status == py_trees.common.Status.INVALID)
    print("task_two.status == py_trees.common.Status.RUNNING")
    assert(task_two.status == py_trees.common.Status.RUNNING)
