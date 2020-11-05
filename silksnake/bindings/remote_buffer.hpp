#ifndef SILKSNAKE_BINDINGS_REMOTE_BUFFER_H_
#define SILKSNAKE_BINDINGS_REMOTE_BUFFER_H_

#include <ostream>

#include <pybind11/pybind11.h>
#include <silkworm/db/state_buffer.hpp>

namespace py = pybind11;

using namespace silkworm;

class RemoteBuffer : public db::StateBuffer {
public:
    explicit RemoteBuffer(const py::handle state_reader, std::optional<uint64_t> historical_block = std::nullopt)
        : state_reader_(state_reader) {}

    /** @name Readers */
    ///@{
    std::optional<Account> read_account(const evmc::address& address) const noexcept override;

    Bytes read_code(const evmc::bytes32& code_hash) const noexcept override;

    std::optional<BlockHeader> read_header(uint64_t block_number, const evmc::bytes32& block_hash) const noexcept override;

    evmc::bytes32 read_storage(const evmc::address& address, uint64_t incarnation, const evmc::bytes32& key) const noexcept override;

    uint64_t previous_incarnation(const evmc::address& address) const noexcept override;
    ///@}

    void insert_header(const BlockHeader& block_header) override {};

    void insert_receipts(uint64_t block_number, const std::vector<Receipt>& receipts) override {};

    /** @name State changes */
    ///@{
    void begin_block(uint64_t block_number) override {}

    void update_account(const evmc::address& address, std::optional<Account> initial, std::optional<Account> current) override {}

    void update_account_code(
        const evmc::address& address,
        uint64_t incarnation,
        const evmc::bytes32& code_hash,
        ByteView code
    ) override {}

    void update_storage(
        const evmc::address& address,
        uint64_t incarnation,
        const evmc::bytes32& key,
        const evmc::bytes32& initial,
        const evmc::bytes32& current
    ) override {}

    void end_block() override {}
    ///@}

private:
    const py::handle state_reader_;
};

std::ostream& operator<<(std::ostream& out, const RemoteBuffer& s);

void bind_remote_buffer(py::module_& module);

#endif  // SILKSNAKE_BINDINGS_REMOTE_BUFFER_H_
