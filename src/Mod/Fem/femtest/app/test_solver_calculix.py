# ***************************************************************************
# *   Copyright (c) 2018 Bernd Hahnebach <bernd@bimstatik.org>              *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "Solver calculix FEM unit tests"
__author__ = "Bernd Hahnebach"
__url__ = "http://www.freecadweb.org"

import unittest
from os.path import join

import FreeCAD

import femsolver.run
from . import support_utils as testtools
from .support_utils import fcc_print


class TestSolverCalculix(unittest.TestCase):
    fcc_print("import TestSolverCalculix")

    # ********************************************************************************************
    def setUp(
        self
    ):
        # setUp is executed before every test

        # new document
        self.document = FreeCAD.newDocument(self.__class__.__name__)

        # more inits
        self.mesh_name = "Mesh"

    # ********************************************************************************************
    def tearDown(
        self
    ):
        # tearDown is executed after every test
        FreeCAD.closeDocument(self.document.Name)

    # ********************************************************************************************
    def test_00print(
        self
    ):
        # since method name starts with 00 this will be run first
        # this test just prints a line with stars

        fcc_print("\n{0}\n{1} run FEM TestSolverFrameWork tests {2}\n{0}".format(
            100 * "*",
            10 * "*",
            55 * "*"
        ))

    # ********************************************************************************************
    def test_solver_calculix(
        self
    ):
        from femexamples.boxanalysis_static import setup
        setup(self.document, "calculix")
        self.calculix_inputfile_writing_test("box_static")

    # ********************************************************************************************
    def calculix_inputfile_writing_test(
        self,
        base_name
    ):

        self.document.recompute()

        # start
        fcc_print(
            "\n------------- Start of FEM CalculiX tests for {} -------"
            .format(base_name)
        )

        # get analysis working directory and save FreeCAD file
        working_dir = testtools.get_fem_test_tmp_dir("solver_calculix_" + base_name)
        save_fc_file = join(working_dir, base_name + ".FCStd")
        fcc_print("Save FreeCAD file to {} ...".format(save_fc_file))
        self.document.saveAs(save_fc_file)

        # write input file
        machine = self.document.SolverCalculiX.Proxy.createMachine(
            self.document.SolverCalculiX,
            working_dir,
            True  # set testmode to True
        )
        machine.target = femsolver.run.PREPARE
        machine.start()
        machine.join()  # wait for the machine to finish

        # compare input file with the given one
        inpfile_given = join(
            testtools.get_fem_test_home_dir(),
            "calculix",
            (base_name + ".inp")
        )
        inpfile_totest = join(
            working_dir,
            self.mesh_name + ".inp"
        )
        fcc_print(
            "Comparing {}  to  {}"
            .format(inpfile_given, inpfile_totest)
        )
        ret = testtools.compare_inp_files(
            inpfile_given,
            inpfile_totest
        )
        self.assertFalse(
            ret,
            "CalculiX write_inp_file for {0} test failed.\n{1}".format(base_name, ret)
        )

        # end
        fcc_print(
            "--------------- End of FEM CalculiX tests for {} ---------"
            .format(base_name)
        )
