require "json"
require "haml"

groups = JSON.parse(File.read("tests.json"))

locals = {
  :var   => "value",
  :first => "a",
  :last  => "z"
}

groups.each do |group|
  name = group[0]
  expectations = group[1]
  describe "When handling #{name}," do
    expectations.each do |input, expected|
      it "should render \"#{input}\" as \"#{expected}\"" do
        engine = Haml::Engine.new(input)
        engine.render(Object.new, locals).chomp.should == expected
      end
    end
  end
end


