#include <algorithm>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <silkworm/types/block.hpp>

#include "block.hpp"
#include "transaction.hpp"
#include "types.hpp"
#include "uint256_type_caster.hpp"

namespace py = pybind11;

using namespace silkworm;

std::ostream& operator<<(std::ostream& out, const BlockHeader& bh) {
    out << "parent_hash=" << bh.parent_hash;
    out << " ommers_hash=" << bh.ommers_hash;
    out << " beneficiary=" << bh.beneficiary;
    out << " state_root=" << bh.state_root;
    out << " transactions_root=" << bh.transactions_root;
    out << " receipts_root=" << bh.receipts_root;
    out << " logs_bloom=" << bh.logs_bloom;
    out << " difficulty=" << bh.difficulty;
    out << " number=" << bh.number;
    out << " gas_limit=" << bh.gas_limit;
    out << " gas_used=" << bh.gas_used;
    out << " timestamp=" << bh.timestamp;
    out << " mix_hash=" << bh.mix_hash;
    out << " nonce=" << bh.nonce;
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
            const std::string& logs_bloom_bytes,
            intx::uint256 difficulty,
            uint64_t number,
            uint64_t gas_limit,
            uint64_t gas_used,
            uint64_t timestamp,
            evmc::bytes32 mix_hash,
            const std::string& nonce_bytes) {
                Bloom logs_bloom{};
                std::copy(logs_bloom_bytes.begin(), logs_bloom_bytes.end(), logs_bloom.begin());
                std::array<uint8_t, 8> nonce{};
                std::copy(nonce_bytes.begin(), nonce_bytes.end(), nonce.begin());
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
