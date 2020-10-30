#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/types/block.hpp>

#include "transaction.hpp"
#include "types.hpp"
#include "uint256_type_caster.hpp"

namespace py = pybind11;

using namespace silkworm;

template<typename T, std::size_t N>
std::ostream& operator<<(std::ostream& out, const std::array<T, N>& a) {
    std::cout << "a.size=" << a.size();
    if (!a.empty()) {
        out << "[";
        std::for_each(a.begin(), a.end(), [&out](const T& t) { out << t; });
        out << "]";
    }
    return out;
}

template<typename T>
std::ostream& operator<<(std::ostream& out, const std::vector<T>& v) {
    if (!v.empty()) {
        out << "[";
        std::for_each(v.begin(), v.end(), [&out](const T& t) { out << t; });
        out << "]";
    }
    return out;
}

std::ostream& operator<<(std::ostream& out, const BlockHeader& h) {
    out << "parent_hash=" << h.parent_hash;
    out << " ommers_hash=" << h.ommers_hash;
    out << " beneficiary=" << h.beneficiary;
    out << " state_root=" << h.state_root;
    out << " transactions_root=" << h.transactions_root;
    out << " receipts_root=" << h.receipts_root;
    out << " logs_bloom=" << h.logs_bloom;
    out << " difficulty=" << h.difficulty;
    out << " number=" << h.number;
    out << " gas_limit=" << h.gas_limit;
    out << " gas_used=" << h.gas_used;
    out << " timestamp=" << h.timestamp;
    out << " mix_hash=" << h.mix_hash;
    out << " nonce=" << h.nonce;
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
                auto header = BlockHeader{};
                header.parent_hash = parent_hash;
                header.ommers_hash = ommers_hash;
                header.beneficiary = beneficiary;
                header.state_root = state_root;
                header.transactions_root = transactions_root;
                header.receipts_root = receipts_root;
                header.logs_bloom = logs_bloom;
                header.difficulty = difficulty;
                header.number = number;
                header.gas_limit = gas_limit;
                header.gas_used = gas_used;
                header.timestamp = timestamp;
                header.mix_hash = mix_hash;
                header.nonce = nonce;
                return header;
        }))
        .def("__repr__", [](const BlockHeader& h) {
            std::ostringstream oss;
            oss << "<silkworm::BlockHeader " << h << ">";
            return oss.str();
        });

    py::class_<BlockBody>(m, "BlockBody")
        .def(py::init())
        .def(py::init<
            std::vector<Transaction>&,
            std::vector<BlockHeader>&
            >())
        .def("__repr__", [](const BlockBody& b) {
            std::ostringstream oss;
            oss << "<silkworm::BlockBody transactions=[" << b.transactions << "], ommers=[" << b.ommers << "]>";
            return oss.str();
        });

    py::class_<Block, BlockBody>(m, "Block")
        .def(py::init<
            std::vector<Transaction>&,
            std::vector<BlockHeader>&,
            const BlockHeader &
            >())
        .def("__repr__", [](const Block& b) {
            std::ostringstream oss;
            oss << "<silkworm::Block transactions=[" << b.transactions << "], ommers=[" << b.ommers << "], header={" << b.header << "}>";
            return oss.str();
        });
}
