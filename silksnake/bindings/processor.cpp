#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/types/block.hpp>
#include <silkworm/chain/config.hpp>

#include "chain_config.hpp"
#include "processor.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const ExecutionProcessor& p) {
    out << &p;
    return out;
}

void bind_execution_processor(pybind11::module_ &m) {
    pybind11::class_<ExecutionProcessor>(m, "ExecutionProcessor")
        .def(py::init([](const Block& block, IntraBlockState& state, const ChainConfig& config) {
            return std::make_unique<ExecutionProcessor>(block, state, config);
        }))
        .def("cumulative_gas_used", &ExecutionProcessor::cumulative_gas_used)
        .def("execute_block", &ExecutionProcessor::execute_block)
        .def("execute_transaction", &ExecutionProcessor::execute_transaction)
        .def("__repr__", [](const ExecutionProcessor& p) {
            std::ostringstream oss;
            oss << "<silkworm::ExecutionProcessor " << p << ">";
            return oss.str();
        });
}
