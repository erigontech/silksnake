#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/types/block.hpp>

#include "transaction.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const BlockHeader& h) {
    out << "<silkworm::BlockHeader>";
    return out;
}

template<typename T>
std::ostream& operator<<(std::ostream& out, const std::vector<T>& v) {
    if (!v.empty()) {
        out << "[";
        std::for_each(v.begin(), --v.end(), [&out](const T& t) { out << t; });
        out << v.back() << "]";
    }
    return out;
}

void bind_block(py::module_ &m) {
    py::class_<BlockHeader>(m, "BlockHeader")
        .def(py::init())
        .def(py::init([](
            evmc::bytes32 parent_hash,
            evmc::bytes32 ommers_hash,
            evmc::address beneficiary,
            evmc::bytes32 state_root,
            evmc::bytes32 transactions_root,
            evmc::bytes32 receipts_root,
            Bloom logs_bloom,
            intx::uint256 difficulty,
            uint64_t number,
            uint64_t gas_limit,
            uint64_t gas_used,
            uint64_t timestamp,
            evmc::bytes32 mix_hash,
            std::array<uint8_t, 8> nonce) {
                return BlockHeader{};
        }))
        .def("__repr__", [](const BlockHeader& h) {
            std::ostringstream oss;
            oss << h;
            return oss.str();
        });

    py::class_<Block>(m, "Block")
        .def(py::init<
            std::vector<Transaction>&,
            std::vector<BlockHeader>&,
            const BlockHeader &
            >())
        .def("__repr__", [](const Block& b) {
            std::ostringstream oss;
            oss << "<silkworm::Block transactions=[" << b.transactions << "], ommers=[" << b.ommers << "]>";
            return oss.str();
        });
}
