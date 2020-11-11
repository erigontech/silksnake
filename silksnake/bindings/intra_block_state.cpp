#include <optional>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/types/transaction.hpp>

#include "intra_block_state.hpp"
#include "remote_buffer.hpp"
#include "types.hpp"
#include "uint256_type_caster.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const IntraBlockState& s) {
    out << &s;
    return out;
}

void bind_intra_block_state(py::module_ &m) {
    py::class_<IntraBlockState>(m, "IntraBlockState")
        .def(py::init([](RemoteBuffer& db) {
            return std::make_unique<IntraBlockState>(db);
        }))
        .def("__repr__", [](const IntraBlockState& s) {
            std::ostringstream oss;
            oss << "<silkworm::IntraBlockState " << s << ">";
            return oss.str();
        });
}