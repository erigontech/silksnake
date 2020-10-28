#include <pybind11/pybind11.h>

#include <sstream>

#include <silkworm/chain/config.hpp>
#include <silkworm/execution/processor.hpp>

namespace py = pybind11;

using namespace silkworm;

void bind_execution_processor(py::module_ &m) {
    py::class_<ExecutionProcessor>(m, "ExecutionProcessor")
        //.def(py::init<const Block&, IntraBlockState&, const ChainConfig&>(),
        //    py::arg("block"), py::arg("state"), py::arg("config")=kMainnetConfig)
        .def("cumulative_gas_used", &ExecutionProcessor::cumulative_gas_used)
        .def("__repr__", [](const ExecutionProcessor& p) {
            std::ostringstream oss;
            oss << "<silkworm::ExecutionProcessor"
                << " >";
            return oss.str();
        });
}
