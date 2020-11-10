#include <optional>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/types/log.hpp>
#include <silkworm/types/receipt.hpp>

#include "types.hpp"
#include "uint256_type_caster.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const Log& l) {
    out << "address=" << l.address
        << " topics=" << l.topics
        << " data=" /*<< l.data*/;
    return out;
}

std::ostream& operator<<(std::ostream& out, const Receipt& r) {
    out << "success=" << r.success
        << " cumulative_gas_used=" << r.cumulative_gas_used
        << " bloom=" << r.bloom
        << " logs=" << r.logs;
    return out;
}

void bind_receipt(py::module_& module) {
    py::class_<Receipt>(module, "Receipt")
        .def(py::init())
        .def_readwrite("success", &Receipt::success)
        .def_readwrite("cumulative_gas_used", &Receipt::cumulative_gas_used)
        .def_readwrite("bloom", &Receipt::bloom)
        .def_readwrite("logs", &Receipt::logs)
        .def("__repr__", [](const Receipt& r) {
            std::ostringstream oss;
            oss << "<silkworm::Receipt " << r << ">";
            return oss.str();
        });
}
