#ifndef SILKSNAKE_BINDINGS_TYPES_H_
#define SILKSNAKE_BINDINGS_TYPES_H_

#include <array>
#include <iomanip>
#include <ostream>
#include <type_traits>

#include <evmone/evmc/include/evmc/evmc.hpp>

template<typename T, std::size_t N>
std::ostream& operator<<(std::ostream& out, const std::array<T, N>& a) {
    if (!a.empty()) {
        out << "[";
        std::for_each(a.begin(), a.end(), [&out](const T& t) {
            if constexpr (std::is_integral<T>::value)
                out << std::hex << std::setw(2) << std::setfill('0') << int(t);
            else
                out << t;
        });
        out << "]";
    }
    return out;
}

template<typename T>
std::ostream& operator<<(std::ostream& out, const std::vector<T>& v) {
    if (!v.empty()) {
        out << "[";
        std::for_each(v.begin(), v.end(), [&out](const T& t) {
            if constexpr (std::is_integral<T>::value)
                out << std::hex << std::setw(2) << std::setfill('0') << int(t);
            else
                out << t;
        });
        out << "]";
    }
    return out;
}

std::ostream& operator<<(std::ostream& out, intx::uint256 i);
std::ostream& operator<<(std::ostream& out, const evmc::address& a);
std::ostream& operator<<(std::ostream& out, const evmc::bytes32& b);

#endif  // SILKSNAKE_BINDINGS_TYPES_H_