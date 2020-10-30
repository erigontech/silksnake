#include <iomanip>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/types/block.hpp>

#include "transaction.hpp"
#include "types.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, intx::uint256 i) {
    out << "0x";
    for (auto q : {i.hi.hi, i.hi.lo, i.lo.hi, i.lo.lo}) {
        out << std::hex << std::setw(16) << std::setfill('0') << uint64_t(q);
    }
    out << std::dec;
    return out;
}

std::ostream& operator<<(std::ostream& out, const evmc::address& a) {
    out << "0x";
    for (const auto& b : a.bytes) {
        out << std::hex << std::setw(2) << std::setfill('0') << int(b);
    }
    out << std::dec;
    return out;
}

std::ostream& operator<<(std::ostream& out, const evmc::bytes32& b32) {
    out << "0x";
    for (const auto& b : b32.bytes) {
        out << std::hex << std::setw(2) << std::setfill('0') << int(b);
    }
    out << std::dec;
    return out;
}

void bind_types(py::module_ &m) {
    py::class_<evmc::address>(m, "EvmAddress")
        .def(py::init())
        .def(py::init([](const std::string& bytes) {
            evmc::address a{};
            std::memcpy(a.bytes, bytes.data(), std::min(bytes.size(), silkworm::kAddressLength));
            return a;
        }))
        .def_property("bytes", [](const evmc::address& a) { return a.bytes; }, [](evmc::address& a, const std::string& bytes) {
            std::memcpy(a.bytes, bytes.data(), std::min(bytes.size(), silkworm::kAddressLength));
        })
        .def("__repr__", [](const evmc::address& a) {
            std::ostringstream oss;
            oss << "<silkworm::evmc::address " << a << ">";
            return oss.str();
        });

    py::class_<evmc::bytes32>(m, "EvmBytes32")
        .def(py::init())
        .def(py::init([](const std::string& bytes) {
            evmc::bytes32 b32{};
            std::memcpy(b32.bytes, bytes.data(), std::min(bytes.size(), silkworm::kHashLength));
            return b32;
        }))
        .def_property("bytes", [](const evmc::bytes32& b32) { return b32.bytes; }, [](evmc::bytes32& b32, const std::string& bytes) {
            std::memcpy(b32.bytes, bytes.data(), std::min(bytes.size(), silkworm::kHashLength));
        })
        .def("__repr__", [](const evmc::bytes32& b32) {
            std::ostringstream oss;
            oss << "<silkworm::evmc::bytes32 " << b32 << ">";
            return oss.str();
        });
}
