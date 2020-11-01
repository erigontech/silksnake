#include <optional>
#include <sstream>

#include <pybind11/pybind11.h>
#include <silkworm/db/buffer.hpp>

#include "buffer.hpp"
#include "types.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const db::Buffer& b) {
    out << "<silkworm::db::Buffer"
        << " >";
    return out;
}

void bind_buffer(py::module_ &m) {
    py::class_<db::Buffer>(m, "Buffer")
        .def(py::init([](lmdb::Transaction* txn, std::optional<uint64_t> historical_block = std::nullopt) {
            return std::make_unique<db::Buffer>(txn, historical_block);
        }))
        .def("__repr__", [](const db::Buffer& b) {
            std::ostringstream oss;
            oss << b;
            return oss.str();
        });
}
