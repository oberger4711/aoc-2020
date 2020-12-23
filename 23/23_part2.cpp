#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

// This is some kind of cyclic linked list data structure.
struct Cup {
  Cup* next = nullptr;
  int label = 0;
};

inline void print_cups(const Cup* c_start) {
  const auto* c_current = c_start;
  do {
    std::cout << c_current->label + 1 << " ";
    c_current = c_current->next;
  } while (c_current != c_start);
  std::cout << "\n";
}

int main() {
  // ################## TEST PART 1 ##################
  //std::vector<int> input = {2, 7, 8, 0, 1, 4, 3, 5, 6}; // NOTE: Converted to 0 based
  //constexpr int NUM_CUPS = 9;
  //constexpr int NUM_ITERATIONS = 10;


  // ################## TEST PART 2 ##################
  //std::vector<int> input = {2, 7, 8, 0, 1, 4, 3, 5, 6}; // NOTE: Converted to 0 based
  //constexpr int NUM_CUPS = 1000000;
  //constexpr int NUM_ITERATIONS = 10000000;


  // ################# THE REAL DEAL #################
  std::vector<int> input = {2, 1, 5, 4, 0, 8, 3, 6, 7}; // NOTE: Converted to 0 based.
  constexpr int NUM_CUPS = 1000000; // Must be < input.size()
  constexpr int NUM_ITERATIONS = 10000000;

  // Initialize cups.
  std::vector<Cup> cups(NUM_CUPS); // Allows random access to a cup given its label.
  // Initialize cups.
  for (int l_current = 0; l_current < NUM_CUPS; ++l_current) {
    const int l_next = (l_current + 1) % NUM_CUPS;
    cups[l_current].next = &(cups[l_next]);
    cups[l_current].label = l_current;
  }
  // Reinitialize cups given by input.
  for (size_t i_input = 0; i_input < input.size(); ++i_input) {
    const int l_current = input[i_input];
    const int l_next = input[(i_input + 1) % input.size()];
    cups[l_current].next = &(cups[l_next]);
  }
  // Fix transitions.
  if (input.size() < NUM_CUPS) {
    // As in part 2: Generated the rest.
    cups[input.back()].next = &(cups[input.size()]);
    cups.back().next = &(cups[input.front()]);
  }
  else {
    // As in part 1: All cups given by input.
    cups[input.back()].next = &(cups[input.front()]);
  }

  // Game
  auto* c_current = &(cups[input[0]]);
  for (size_t round = 0; round < NUM_ITERATIONS; ++round) {
    // Pick up.
    auto* first_picked_up = c_current->next;
    auto* last_picked_up = first_picked_up->next->next;
    c_current->next = last_picked_up->next; // Unlink the picked up cups.
    // Find destination.
    int l_place_dest = c_current->label;
    do {
      --l_place_dest;
      if (l_place_dest < 0) {
        l_place_dest = NUM_CUPS - 1;
      }
    } while ((first_picked_up->label == l_place_dest) ||
             (first_picked_up->next->label == l_place_dest) ||
             (last_picked_up->label == l_place_dest));
    auto* c_place_before = &(cups[l_place_dest]);
    auto* c_place_after = c_place_before->next;
    // Place the previously picked up cups.
    c_place_before->next = first_picked_up;
    last_picked_up->next = c_place_after;
    // Select new current cup.
    c_current = c_current->next;
  }
  //print_cups(c_current);

  std::cout << "Cups after cup 1: " << cups[0].next->label + 1 << ", " << cups[0].next->next->label + 1 << "\n";
  //std::cout << "Part 2: " << (cups[0].next->label + 1) * (cups[0].next->next->label + 1) << "\n";
  return EXIT_SUCCESS;
}
